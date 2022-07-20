from flask import Flask, render_template,request,redirect,url_for,session,flash
import psycopg2
import urllib.request
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret"

DB_HOST="localhost"
DB_NAME="homeappliances"
DB_USER="postgres"
DB_PASS="test123"

conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)

FILE = 'static/file'
PHOTO = 'static/photo'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = FILE
app.config['UPLOAD_FOLDER_IMAGE'] = PHOTO

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/retailerlogin",methods=['GET','POST'])
def retailer():
    if 'check' in session:
        return redirect(url_for('display'))
    else:
        return redirect(url_for('retailerlogin'))

@app.route('/retailerloginprocess', methods=['GET', 'POST'])
def retailerlogin1():
    cur=conn.cursor()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cur.execute(f"SELECT * FROM retailer WHERE email='{email}'")
        account=cur.fetchone()
        if account:
            passwordhash = account[2]
            checkpassword = check_password_hash(passwordhash, password)
            if checkpassword:
                session['check'] = True
                session['email'] = account[1]
                session['password'] = account[2]
                flash("You are Loged In Successfully!")
                return redirect(url_for('display'))
            else:
                error = 'Invalid retailer Email And Password'
                return render_template('retailerlogin.html',error=error)
        else:
            error = "You need to first login"
            return render_template('retailerlogin.html',error=error)

    cur.close()
    return render_template('retailerlogin.html')


@app.route("/Retailer_Login")
def retailerlogin():
    return render_template("retailerlogin.html")

@app.route("/retailermaster",methods=['GET','POST'])
def display():
    if session['check']:
        cur=conn.cursor()
        cur.execute(f"SELECT * FROM customer_profile,customer where customer.id = customer_profile.customerid order by customer.id desc")
        account = cur.fetchall()
        return render_template("retailermaster.html", data = account)
    else:
        return redirect(url_for('retailerlogin'))

@app.route("/addretailer",methods=['GET','POST'])
def retailerinsert1():
    return render_template("retailerinsert.html")

@app.route("/new_reatailer_added", methods=['GET','POST'])
def insertretailer():
    cur = conn.cursor()
    email=request.form.get("email")
    password=request.form.get("password")
    confirmpassword = request.form.get("confirmpassword")
    hashed_password = generate_password_hash(password)
    if password == confirmpassword:
        cur.execute(f"INSERT INTO retailer (email,password) VALUES ('{email}','{hashed_password}')")
        conn.commit()
    else:
        error = "Password and Confirm password doesn't match..."
        return render_template("retailerinsert.html", error=error)

    flash("You are now our shop retailer. Congratulation!")
    return redirect(url_for('retailerlogin'))

@app.route("/update-customer-password/<int:customer_id>")
def get_password(customer_id):
    if session['check']:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM customer_profile,customer where customer.id = '{customer_id}'and customer_profile.customerid = '{customer_id}'")
        account = cur.fetchone()

        return render_template("customerpassword.html", account=account)
    else:
        return redirect(url_for('display'))

@app.route("/update-password-of-customer/<int:customer_id>", methods=["GET", "POST"])
def updatepassword(customer_id):
    if session['check']:
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        if request.method == "POST":
            if password == confirmpassword:
                conformpassword()
            else:
                error = "Password and Confirm password doesn't match..."
                cur = conn.cursor()
                cur.execute(f"SELECT * FROM customer_profile,customer WHERE customer.id = '{customer_id}' and customer_profile.customerid = '{customer_id}'")
                account = cur.fetchone()
                return render_template("customerpassword.html", account=account, error=error)
    else:
        return redirect(url_for('retailer'))

    flash("This Customer Password Successfully Changed")
    return redirect(url_for('display'))

def conformpassword():
    cur = conn.cursor()
    customerid = request.form.get("customerid")
    password = request.form.get("password")
    hashed_password = generate_password_hash(password)
    cur.execute(f"""UPDATE customer set password='{hashed_password}' WHERE id='{customerid}' """)
    conn.commit()
    cur.close()
    return redirect(url_for('display'))	

@app.route("/Create-customer",methods=['GET','POST'])
def newcustomer():
    return render_template("addcustomer.html")

@app.route("/customer_added", methods=['GET','POST'])
def insertcustomer():
    if session['check']:
        cur = conn.cursor()
        customernm = request.form.get('customername')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        cur.execute(f"SELECT * FROM customer where email = '{email}'")
        customeremail = cur.fetchone()
        cur.execute(f"SELECT * FROM customer where customername = '{customernm}'")
        customername = cur.fetchone()
        cur.close()


        if customeremail:
            error = "This email is already exists give another E-mail id"
            return render_template("addcustomer.html", error=error)
        if customername:
            error = "This customername is already exists give another customername"
            return render_template("addcustomer.html", error=error)
        if request.method == "POST":
            if password == confirmpassword:
                newcustomer1()
            else:
                error = "Password and Confirm password doesn't match..."
                return render_template("addcustomer.html", error=error)
    else:
        return redirect(url_for('retailer'))
    return redirect(url_for('display'))

def newcustomer1():
    cur = conn.cursor()
    email = request.form.get('email')
    password = request.form.get('password')
    customername = request.form.get('customername')
    hashed_password = generate_password_hash(password)
    cur.execute(f"""INSERT INTO customer (email,password,customername) VALUES ('{email}','{hashed_password}','{customername}')""")
    conn.commit()
    cur.execute("SELECT max(id) FROM customer")
    new_id = cur.fetchone()
    cur.execute(f"""INSERT INTO customer_profile (customerid) VALUES ('{new_id[0]}')""")
    conn.commit()
    cur.close()
    flash("New Customer added Successfully.")
    return redirect(url_for('display'))

@app.route("/update-customer-profile/<int:customer_id>")
def fetchupdatecustomer(customer_id):
    if session['check']:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM customer_profile,customer WHERE customer.id = '{customer_id}' and customer_profile.customerid = '{customer_id}'")
        account = cur.fetchone()
        cur.close()
        return render_template("customeredit.html", account=account)
    else:
        return redirect(url_for('retailer'))

@app.route("/update",methods=["POST"])
def updatecustomer():
    if session['check']:
        if request.method == "POST":
            cur = conn.cursor()
            customerid = request.form.get("customerid")
            fname = request.form.get("firstname")
            lname = request.form.get("lastname")
            dob = request.form.get("dateofbirth")
            mobile = request.form.get("mobilenumber")
            gender = request.form.get("gender")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            zipcode = request.form.get("zipcode")
            email = request.form.get("email")
            dateupdate = datetime.date.today()
            customername = request.form.get("customername")
            cur.execute(f"""UPDATE customer_profile set firstname='{fname}', lastname='{lname}', dateofbirth='{dob}',mobilenumber='{mobile}', gender='{gender}', address='{address}', city='{city}',state='{state}', zipcode='{zipcode}',profileupdatedate='{dateupdate}' WHERE customerid='{customerid}'""")
            cur.execute(f"""UPDATE customer set customername='{customername}', email='{email}' WHERE id='{customerid}'""")
            conn.commit()
            cur.close()
            flash("Customer Record Update Successfully.")
            return redirect(url_for('display'))

    else:
        return redirect(url_for('retailer'))





@app.route("/Delete-customer-profile/<int:customer_id>")
def deleterecord(customer_id):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM customer_profile where customerid = '{customer_id}'")
    cur.execute(f"DELETE FROM customer where id = '{customer_id}'")
    conn.commit()
    cur.close()
    flash("Customer Record Delete Successfully.")
    return redirect(url_for('display'))

@app.route("/Customer_Login")
def customerlogin():
    return render_template("customerlogin.html")

@app.route("/customerlogin",methods=['GET','POST'])
def customer():
    if 'checkcustomer' in session:
        return redirect(url_for('display1'))
    else:
        return redirect(url_for('customerlogin'))

@app.route('/customerloginprocess', methods=['GET', 'POST'])
def customerlogin1():
    cur=conn.cursor()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form :
        email = request.form['email']
        password = request.form['password']

        cur.execute(f"SELECT * FROM customer WHERE email='{email}'")
        account=cur.fetchone()

        if account:
            passwordhash = account[2]
            checkpassword = check_password_hash(passwordhash, password)
            if checkpassword:
                session['checkcustomer'] = True
                session['id'] = account[0]
                session['email'] = account[1]
                session['password'] = account[2]
                flash("Your Mostly Welcome")
                return redirect(url_for('display1'))
            else:
                error = "Invalid customer Details"
                return render_template('customerlogin.html',error=error)
    cur.close()
    return render_template('customerlogin.html')

@app.route("/Customer_Home_Page",methods=['GET','POST'])
def display1():
    if session['checkcustomer']:
        return render_template("customerhome.html")
    else:
        return redirect(url_for('customerlogin'))

@app.route("/customer-Profile-Page",methods=['GET','POST'])
def profile():
    if session['checkcustomer']:
        cur = conn.cursor()
        customerid = session['id']
        cur.execute(f"SELECT * FROM customer_profile,customer where customer.id ='{customerid}' and customer_profile.customerid='{customerid}'")
        account = cur.fetchone()
        return render_template("customerprofile.html", account=account)
    else:
        return redirect(url_for('customer'))

@app.route("/update-customer-profile")
def fetchupdatecustomer1():
    customer_id=session['id']
    if session['checkcustomer']:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM customer_profile,customer WHERE customer.id = '{customer_id}' and customer_profile.customerid = '{customer_id}'")
        account = cur.fetchone()
        cur.close()
        return render_template("customersideedit.html",account=account)
    else:
        return redirect(url_for('customer'))

@app.route("/update by customer",methods=["GET","POST"])
def updatecustomer1():
    if session['checkcustomer']:
        if request.method == "POST":
            customerid = request.form.get("customerid")
            fname = request.form.get("firstname")
            lname = request.form.get("lastname")
            dob = request.form.get("dateofbirth")
            mobile = request.form.get("mobilenumber")
            gender = request.form.get("gender")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            zipcode = request.form.get("zipcode")
            customername = request.form.get("customername")
            email = request.form.get("email")
            file = request.files['file']
            image = request.files['image']
            dateupdate = datetime.date.today()
            cur = conn.cursor()
            if request.method == "POST":
                filename = secure_filename(file.filename)
                imagename = secure_filename(image.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image.save(os.path.join(app.config['UPLOAD_FOLDER_IMAGE'], imagename))
                cur.execute(f"""UPDATE customer_profile set firstname='{fname}', lastname='{lname}', dateofbirth='{dob}',mobilenumber='{mobile}', gender='{gender}', address='{address}', city='{city}',state='{state}', zipcode='{zipcode}',profileupdatedate='{dateupdate}',fileupload='{filename}',imageupload='{imagename}' WHERE customerid='{customerid}'""")
                cur.execute(f"""UPDATE customer set customername='{customername}', email='{email}' WHERE id='{customerid}'""")
                conn.commit()
                cur.close()
                flash("Your Record update Successfully.")
                return redirect(url_for('profile'))
    else:
        return redirect(url_for('customer'))

@app.route("/logout_Reailer")
def logout():
    session['check']=False
    flash("Retailer Logout Successfully.")
    return render_template("index.html")

@app.route("/logout_Customer")
def logoutcustomer():
    session['checkcustomer']=False
    flash("Customer Logout Successfully.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
