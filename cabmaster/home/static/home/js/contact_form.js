

const sendButton = document.querySelector('#contact-button');
const sendButtonIcon = document.querySelector('#contact-send-icon');

const nameInput = document.querySelector('#id_name');
const email = document.querySelector('#id_email');
const phone = document.querySelector('#id_phone_number');

const subject = document.querySelector('#id_subject');
const message = document.querySelector('#id_message');


// Adding backround to the input when it is filled
const inputs = document.querySelectorAll('.contact-field');

inputs.forEach(input => {
    input.addEventListener('input', function (e) {
        if (e.target.value.length > 0) {
            input.style.background = '#0c4d8a';
            input.style.color = 'white';
        } else {
            input.style.background = 'white';
            input.style.color = 'black';
        }
    });

});


phone.addEventListener('input', (e) => {
    const phoneNumber = e.target.value;
    controlPhoneInput(e, phoneNumber);
});

email.addEventListener('input', (e) => {
    const emailValue = e.target.value;
    const valid = isValidEmail(emailValue);

    if (valid) {
        sendButtonIcon.classList = "bi bi-check-lg";
    } else if (!valid) {
        sendButtonIcon.classList = "bi bi-send";
    }
});

sendButton.addEventListener('click', function (e) {
    e.preventDefault();

    csrf = Cookies.get('csrftoken');

    const formData = new FormData();

    formData.append('name', nameInput.value);
    formData.append('email', email.value);
    formData.append('subject', subject.value);
    formData.append('message', message.value);
    formData.append('csrfmiddlewaretoken', csrf);

    if (phone.value.length > 0) {
        const validPhone = isValidPhoneNumber(phone.value);

        if (!validPhone) {
            showMessage('error', 'Le format du numéro de téléphone est invalide.');
            return;
        } else {
            formData.append('phone_number', phone.value);
        }
    }

    const url = 'api/contact/';

    const valid = checkRequiredFields([nameInput, email, subject, message]);

    if (valid.length === 0) {

        // Check if email is valid
        const validEmail = isValidEmail(email.value);

        if (!validEmail) {
            showMessage('error', 'Le format de l\'adresse email est invalide.');
            email.style.background = '#0c4d8a';
            setTimeout(function () {
                email.style.background = 'white';
            }, 2500);
            return;
        }

        postForm(url, formData)
            .then(data => {
                if (data.success === true) {
                    showMessage('success', 'Votre message a bien été envoyé à l\'équipe CabMaster. Nous vous répondrons dans les plus brefs délais.');

                    nameInput.value = '';
                    email.value = '';
                    phone.value = '';
                    subject.value = '';
                    message.value = '';
                    sendButtonIcon.classList = "bi bi-send";

                    inputs.forEach(input => {
                        input.style.background = 'white';
                        input.style.color = 'black';
                    });

                } else if (data.success === false) {
                    showMessage('error', 'Une erreur est survenue, veuillez réessayer plus tard.');
                }
            })
            .catch(error => {
                showMessage('error', 'Une erreur est survenue, veuillez réessayer plus tard.');
                throw new Error('Error while sending the form' + error);
            });
    } else {
        showMessage('warning', 'Merci de remplir les champs obligatoires.');
        valid.forEach(field => {
            field.style.background = '#0c4d8a';
            setTimeout(function () {
                field.style.background = 'white';
            }, 1200);
        });
    }

});