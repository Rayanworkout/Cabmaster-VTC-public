
///// FUNCTIONS /////

///////////////////// EMAIL /////////////////////

const emailRegisterError = document.querySelector('#email-register-message');
const emailRegisterIcon = document.querySelector('#email-register-icon');


let lastRegisterEmail = "";
let emailValid = false;

const debounceRegisterEmail = (email) => {
    clearTimeout(email.timer);

    email.timer = setTimeout(() => {

        if (email.length > 4 && email !== lastRegisterEmail) {
            lastRegisterEmail = email;
            // Using function from login.js
            const valid = isValidEmail(email)

            if (!valid) {
                emailValid = false;
                emailRegisterIcon.setAttribute('name', 'x');
                emailRegisterError.textContent = "Format incorrect, vérifiez votre saisie.";
            } else if (valid) {
                // Email has a valid format
                // I reset the error message
                emailRegisterError.textContent = "";
                // I display check icon
                emailRegisterIcon.setAttribute('name', 'check');
                emailValid = true;

            }
        } else if (email.length < 1) {
            emailRegisterIcon.setAttribute('name', 'user');
            emailRegisterError.textContent = "";
            emailValid = false;
        }

    }, 600); // 0.6 SECONDS
}


///////////////////// PHONE /////////////////////

function checkPhoneNumber(phoneNumber) {
    // Regular expression pattern for French phone numbers
    const frenchPhoneRegex = /^(\+33|0)(6|7)\d{8}$/;

    // Check if the cleaned number matches the pattern
    const isValid = frenchPhoneRegex.test(phoneNumber);

    return isValid;
}


const phoneRegisterError = document.querySelector('#phone-register-message');
const phoneRegisterIcon = document.querySelector('#phone-register-icon');

let lastRegisterPhone = "";
let phoneValid = false;

const debouncePhone = (phoneNumber) => {
    clearTimeout(phoneNumber.timer);

    phoneNumber.timer = setTimeout(() => {

        if (phoneNumber.length > 4 && phoneNumber !== lastRegisterPhone) {
            lastRegisterPhone = phoneNumber;

            const valid = checkPhoneNumber(phoneNumber)

            if (!valid) {
                phoneValid = false;
                phoneRegisterIcon.setAttribute('name', 'x');
                phoneRegisterError.textContent = "Format incorrect, vérifiez votre saisie.";
            } else if (valid) {
                // Phone number has a valid format
                phoneValid = true;
                // I reset the error message
                phoneRegisterError.textContent = "";
                // I display check icon
                phoneRegisterIcon.setAttribute('name', 'check');

            }
        } else if (phoneNumber.length < 1) {
            phoneRegisterIcon.setAttribute('name', 'phone');
            phoneRegisterError.textContent = "";
            phoneValid = false;
        }

    }, 600); // 0.6 SECONDS

}


////// CHECKING FIELDS //////

const emailRegisterField = document.querySelector('#email_register');
const phoneRegisterField = document.querySelector('#phone_register');


emailRegisterField.addEventListener('input', (e) => {
    const email = e.target.value;

    if (!email.timer) {
        email.timer = null;
    }

    debounceRegisterEmail(email);
});


phoneRegisterField.addEventListener('input', (e) => {
    const phoneNumber = e.target.value;

    if (/[^+\d]/.test(phoneNumber)) {
        e.target.value = phoneNumber.replace(/[^+\d]/g, ''); // Remove all non-digit characters except +
    }

    // Check if the number starts with 33
    // If so, I add + to the beginning of the number
    if (/^33/.test(phoneNumber) && phoneNumber.length > 2) {
        e.target.value = '+' + phoneNumber;
    }

    if (!phoneNumber.timer) {
        phoneNumber.timer = null;
    }

    debouncePhone(phoneNumber);
});


////// FORM ANIMATION //////

register1.addEventListener('click', () => {

    // Checking if fields are filled before allowing next step
    const firstNameValid = document.querySelector('#id_first_name').value.length > 2;
    const lastNameValid = document.querySelector('#id_last_name').value.length > 2;

    if (emailValid && phoneValid && firstNameValid && lastNameValid) {
    registerContainer.style.left = "-810px";
    register2Container.style.right = "4px";
    }

});


const backButton1 = document.querySelector('.back1');
const backButton2 = document.querySelector('.back2');

backButton1.addEventListener('click', () => {
    registerContainer.style.left = "4px";
    register2Container.style.right = "-810px";
});

backButton2.addEventListener('click', () => {
    register2Container.style.left = "4px";
    register3Container.style.right = "-810px";
});


lastStep.addEventListener('click', () => {
    register2Container.style.left = "-810px";
    register3Container.style.right = "4px";
});