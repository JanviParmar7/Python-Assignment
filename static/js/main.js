function check() {
    var pass = document.getElementById("password").value;
    //check empty password field
    if (pass == "") {
        document.getElementById("message").innerHTML = "Fill the password Field!";
        return false;
    }
    //minimum password length validation
    else if (pass.length < 8) {
        document.getElementById("message").innerHTML = "Password length must be 8 characters";
        return false;
    }

    //maximum length of password validation
    else if (pass.length > 8) {
        document.getElementById("message").innerHTML = "Password length must be 8 characters";
        return false;
    } else {
        document.getElementById("message").innerHTML = "";
        return true;
    }
}

function checkconfirmpassword() {
    var confirmpass = document.getElementById("conformpassword").value;
    //check empty password field
    if (confirmpass == "") {
        document.getElementById("passwd").innerHTML = "Fill the Confirm password Field!";
        return false;
    } else {
        document.getElementById("passwd").innerHTML = "";
        return true;
    }
}

function checkemail() {
    var e_mail = document.getElementById("email").value;
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (mailformat.test(e_mail)) {
        document.getElementById('mail').innerHTML = "";
        return true;
    }
    // check empty mail field
    if (e_mail == "") {
        document.getElementById("mail").innerHTML = "Fill the email Field!";
        return false;
    } else {
        document.getElementById("mail").innerHTML = "Your E-mail is Invalid";
        return false;
    }
}

function customername1() {
    var customername1 = document.getElementById("customername").value;
    var customname = /^[0-9a-zA-Z]+$/;
    if (customname.test(customername1)) {
        document.getElementById("customer").innerHTML = "";
        return true;
    }
    // check empty customer field
    if (customername1 == "") {
        document.getElementById("customer").innerHTML = "Fill the Customer Name Field";
        return false;
    } else {
        document.getElementById("customer").innerHTML = "Your Customer Name is Invalid";
        return false;
    }
}

function firstname1() {
    var firstname1 = document.getElementById("firstname").value;
    var firstname = /^[A-Za-z]+$/;
    if (firstname.test(firstname1)) {
        document.getElementById("first").innerHTML = "";
        return true;
    }
    // check empty firstname field
    if (firstname1 == "") {
        document.getElementById("first").innerHTML = "Fill the Customer First Name Field";
        return false;
    } else {
        document.getElementById("first").innerHTML = "Your First Name is Invalid";
        return false;
    }
}

function lastname1() {
    var lastname1 = document.getElementById("lastname").value;
    var lastname = /^[a-zA-Z]+$/;
    if (lastname.test(lastname1)) {
        document.getElementById("last").innerHTML = "";
        return true;
    }
    // check empty lastname field
    if (lastname1 == "") {
        document.getElementById("last").innerHTML = "Fill the Customer Last Name Field";
        return false;
    } else {
        document.getElementById("last").innerHTML = "Your Last Name is Invalid";
        return false;
    }
}

function dateofbirth1() {
    var input = document.getElementById("dateofbirth").value;
    var dateofbirth = new Date(input);
    if (input == null || input == '') {
        document.getElementById("datee").innerHTML = "Fill the Date Of Birth Field";
        return false;
    } else {
        //calculate month difference from current date in time
        var month = Date.now() - dateofbirth.getTime();

        //convert the calculated difference in date format
        var agedate = new Date(month);

        //extract year from date
        var year = agedate.getUTCFullYear();

        //now calculate the age of the user
        var age = Math.abs(year - 1970);
        //display the calculated age
        if (age < 18) {
            document.getElementById("datee").innerHTML = "Age should be more than 18 years.Please enter a valid Date of Birth";
            return false;
        } else if (age > 50) {
            document.getElementById("datee").innerHTML = "Age should be Less than 50 years.Please enter a valid Date of Birth";
            return false;
        } else {
            document.getElementById("datee").innerHTML = "";
            return true;
        }
    }
}

function mobilenumber1() {
    var mobilenumber1 = document.getElementById("mobileno").value;
    var m = /^[6789]\d{9}$/;
    if (m.test(mobilenumber1)) {
        document.getElementById("mobile").innerHTML = "";
        return true;
    }
    // check empty mobilenumber field
    if (mobilenumber1 == "") {
        document.getElementById("mobile").innerHTML = "Fill the Mobile Number Field";
        return false;
    }
    //minimum mobile number length validation
    if (mobilenumber1.length < 10) {
        document.getElementById("mobile").innerHTML = "Mobile Number length must be 10 characters";
        return false;
    }

    //maximum length of mobile number validation
    if (mobilenumber1.length > 10) {
        document.getElementById("mobile").innerHTML = "Mobile Number length must be 10 characters";
        return false;
    } else {
        document.getElementById("mobile").innerHTML = "Please enter valid Mobile number!";
        return false;
    }
}

var male = document.getElementById("mal");
var female = document.getElementById("fem");
var checked = document.getElementById("sel").innerHTML;
if (checked == "Male") {
    male.click()
} else if (checked == "Female") {
    female.click()
} else {}


function address1() {
    var address1 = document.getElementById("addresss").value;
    // check empty address field
    if (address1 == "") {
        document.getElementById("add").innerHTML = "Fill the Address Field";
        return false;
    } else {
        document.getElementById("add").innerHTML = "";
        return true;
    }
}

function city1() {
    var city1 = document.getElementById("cityy").value;
    // check empty city field
    if (city1 == "") {
        document.getElementById("citi").innerHTML = "Fill the City Field";
        return false;
    } else {
        document.getElementById("citi").innerHTML = "";
        return true;
    }
}

function state1() {
    var state1 = document.getElementById("statee").value;
    // check empty state field
    if (state1 == "") {
        document.getElementById("stat").innerHTML = "Fill the State Field";
        return false;
    } else {
        document.getElementById("stat").innerHTML = "";
        return true;
    }
}

function zipcode1() {
    var zipcode1 = document.getElementById("zipcodee").value;
    var z = /^[0-9]{6}$/;
    if (z.test(zipcode1)) {
        return true;
    }
    // check empty zipcode field
    else if (zipcode1 == "") {
        document.getElementById("zicode").innerHTML = "Fill the Zipcode Field";
        return false;
    } //minimum zipcode length validation
    else if (zipcode1.length < 6) {
        document.getElementById("zicode").innerHTML = "Zipcode length must be 6 characters";
        return false;
    }

    //maximum zipcode of password validation
    else if (zipcode1.length > 6) {
        document.getElementById("zicode").innerHTML = "Zipcode length must be 6 characters";
        return false;
    } else {
        document.getElementById("zicode").innerHTML = "Please enter Valid Zipcode!";
        return false;
    }
}

function fileupload1() {
    var upload = document.getElementById("fileupload").value;
    // check empty fileupload field
    if (upload == "") {
        document.getElementById("files").innerHTML = "Required to attach file of birth cirtificate";
        return false;
    }
    if (!/\.pdf$/i.test(upload)) {
        document.getElementById("files").innerHTML = "Attach only pdf format file";
        return false;
    }
    else {
        document.getElementById("files").innerHTML = "";
        return true;
    }
}


 function imageupload1()
{
    var fileInput =  document.getElementById('imageupload');
    var filePath = fileInput.value;
    var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if(filePath == "")
    {
        document.getElementById("photo").innerHTML = "Required to attach Profile Picture";
        return false;
    }
    if (!allowedExtensions.exec(filePath))
    {
        document.getElementById("photo").innerHTML = "Attach jpg,jpeg,gif,png format file";
        fileInput.value = '';
        return false;
    }
    else
    {
        document.getElementById("photo").innerHTML = "";
        return true;
    }
}

