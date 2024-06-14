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


// Identifying inputs to autocomplete
const pickupAddressInput = document.querySelector('#home_estimate_start');
const destinationInput = document.querySelector('#home_estimate_end');


// Allow user to estimate a ride
const estimateButton = document.querySelector('#home-estimate-button');
const estimateMessage = document.querySelector('.estimate-message');

// Estimation elements to fill
const cardsEstimationResults = document.querySelector('.estimation-result-cards');
const ecoCard = document.querySelector('.eco-card-content');
const berlineCard = document.querySelector('.berline-card-content');
const vanCard = document.querySelector('.van-card-content');

let lastEstimation = {
    'origin': '',
    'destination': '',
    'courseGrade': '',
}

estimateButton.addEventListener('click', (e) => {


    // At click, we verify if pickup and destination inputs are filled
    if (pickupAddressInput.value.length === 0 || destinationInput.value.length === 0) {
        pickupAddressInput.style.background = '#F43910';
        destinationInput.style.background = '#F43910';

        estimateMessage.textContent = 'Merci de renseigner une adresse de départ et une adresse de destination.';

        // Put it back to normal after 5 seconds
        setTimeout(function () {
            estimateMessage.textContent = "Estimez gratuitement le prix de votre course en 1 clic !";
            pickupAddressInput.style.background = 'white';
            destinationInput.style.background = 'white';

        }, 5000);

        return;
    }

    // NECCESSARY DATA TO ESTIMATE PRICE
    const data = {
        'origin': pickupAddressInput.value,
        'destination': destinationInput.value,
        'courseGrade': "all",
    }

    // Check if the estimation is the same as the last one
    if (JSON.stringify(data) === JSON.stringify(lastEstimation)) {
        return;
    }

    // functions.js
    estimateCoursePrice(data)
        .then((response) => {
            if (response.ok) {
                response.json().then((data) => {
                    // We fill the data of the 3 cards and we show them
                    cardsEstimationResults.style.display = 'block';
                    ecoCard.innerHTML = `
                    <li style="color: black;">Prix estimé : ${data.price[0]} €</li>
                    <li style="color: black;">Distance : ${data.distance_str}</li>
                    <li style="color: black;">Durée : ${data.duration}</li>`;

                    berlineCard.innerHTML = `
                    <li style="color: black;">Prix estimé : ${data.price[1]} €</li>
                    <li style="color: black;">Distance : ${data.distance_str}</li>
                    <li style="color: black;">Durée : ${data.duration}</li>`;

                    vanCard.innerHTML = `
                    <li style="color: black;">Prix estimé : ${data.price[2]} €</li>
                    <li style="color: black;">Distance : ${data.distance_str}</li>
                    <li style="color: black;">Durée : ${data.duration}</li>`;
                });
            } else if (response.status === 403) {
                showMessage('error', 'Limite de demande atteinte, veuillez réessayer plus tard');
            }
        }).catch((error) => {
            showMessage('error', 'Une erreur est survenue, veuillez réessayer plus tard');
            throw new Error(error);
        });

    lastEstimation = data;

});

// Creating autocomplete objects
let autoCompletePickupAddressHome;
let autoCompleteDestinationHome;

// Initializing autocomplete
function initAutocomplete() {
    autoCompletePickupAddressHome = new google.maps.places.Autocomplete(pickupAddressInput, options);
    autoCompleteDestinationHome = new google.maps.places.Autocomplete(destinationInput, options);
};