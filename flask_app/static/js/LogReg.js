//* Register Password
function regPassword() {
    let x = document.getElementById("RegPassword");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

//*Confirm Register Password
function regConfPassword() {
    let x = document.getElementById("RegConPassword");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

// * For the login password
function logPassword() {
    let x = document.getElementById("LoginPassword");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}