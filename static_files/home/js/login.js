

const registerContainer = document.querySelector('#register');
const register2Container = document.querySelector('#register2');
const register3Container = document.querySelector('#register3');

const register1 = document.querySelector('#register-submit1');

const lastStep = document.querySelector('#register-submit2');



/////////////////////// LOGIN ///////////////////////////////


// Variable to check if the user can login
let ableToLogin = false;

const performLogin = async (formData, csrfToken) => {
    if (ableToLogin) {

        // Get the next url
        const nextUrl = new URL(window.location.href).searchParams.get('next');

        await loginUser(formData, csrfToken)
            .then(
                result => {
                    if (result.success === true) {
                        Swal.fire({
                            icon: "success",
                            title: "Connexion réussie, Bienvenue !",
                            toast: true,
                            position: "top-end",
                            showConfirmButton: false,
                            timer: 2000,
                            timerProgressBar: true,
                        })
                        setTimeout(() => {
                            if (nextUrl) {
                                window.location.href = window.location.origin + nextUrl;
                            } else if (!nextUrl) {
                                window.location.href = window.location.origin
                            }


                        }, 2000);
                    } else if (result.status === 403) {
                        showMessage("error", "Limite atteinte, veuillez réessayer plus tard");
                    } else if (!result.success) {
                        showMessage("error", "Email ou mot de passe incorrect");
                    }
                }
            ).catch(error => {
                console.log(error)
            })
    }
}

const loginButton = document.querySelector('#login-button');

// Logo inside the login button
const loginLogo = document.querySelector('#login-logo');


const passwordField = document.querySelector('#id_password');

const emailField = document.querySelector('#id_email');



// Store the last email address that was checked in order not to send the same request twice
let lastEmail = "";



// Event listener for the password input field
emailField.addEventListener('input', (e) => {
    e.preventDefault();
    const email = e.target.value;

    // Check if the email is valid
    const valid = isValidEmail(email);

    if (valid) {
        passwordField.addEventListener('input', (e) => {
            const password = e.target.value;

            strong = isStrongPassword(password, email);

            if (strong) {
                ableToLogin = true;
                loginLogo.classList = "bi bi-check-lg";
            } else if (!strong) {
                ableToLogin = false;
                loginLogo.classList = "bi bi-arrow-up-right-circle";
            }
        });
    }

});


/////////////////////// PERFORMING LOGIN ///////////////////////////////

const loginByKeyboard = async (event) => {
    if (event.keyCode === 13) {

        const email = emailField.value;
        const password = passwordField.value;

        const valid = isValidEmail(email);
        const validPassword = isStrongPassword(password, email);

        if (valid && validPassword) {
            event.preventDefault();
            const formData = new FormData();

            const csrfToken = await Cookies.get('csrftoken');

            formData.append('email', email);
            formData.append('password', password);

            performLogin(formData, csrfToken);
        }


    }
}

// BY HITTING ENTER ON KEYBOARD
passwordField.addEventListener('keydown', loginByKeyboard);
emailField.addEventListener('keydown', loginByKeyboard);


// OR BY CLICKING ON THE LOGIN BUTTON
loginButton.addEventListener('click', async (e) => {
    e.preventDefault();

    const email = emailField.value;
    const password = passwordField.value;

    const valid = isValidEmail(email);
    const validPassword = isStrongPassword(password, email);



    if (valid && validPassword) {

        const formData = new FormData();

        const csrfToken = await Cookies.get('csrftoken');

        formData.append('email', email);
        formData.append('password', password);

        performLogin(formData, csrfToken);

    } else if (!valid) {
        showMessage("warning", "Veuillez entrer une adresse email valide");
    } else if (!validPassword) {
        showMessage("warning", "Veuillez entrer un mot de passe valide");
    }

});



