// GÉRER LE CAS MISE À DISPOSITION


// EMAIL DE CONFIRMATION DE RÉSERVATION


// All mandatory inputs
const mandatoryInputs = document.querySelectorAll('.mandatory');

// All inputs to prevent default enter button
const allInputs = document.querySelectorAll('.prevent');


// Form fields
const customerFirstNameField = document.querySelector('#id_customer_first_name');
const customerLastNameField = document.querySelector('#id_customer_last_name');

const phoneField = document.querySelector('#id_customer_phone_number');
const customerEmailField = document.querySelector('#id_customer_email');

const pickupAddressField = document.querySelector('#id_pickup_address');
const destinationField = document.querySelector('#id_destination');

const happeningDateField = document.querySelector('#id_happening_date');
const happeningTimeField = document.querySelector('#id_happening_time');

const passengersField = document.querySelector('#passengers');
const paymentModeField = document.querySelector('#id_payment_mode');

const bigCases = document.querySelector('#big-cases');
const smallCases = document.querySelector('#small-cases');

const moreInfosField = document.querySelector('#id_more_infos');



// Listening of all fields and prevent defaults of enter button
allInputs.forEach((input) => {
    input.addEventListener('keypress', (e) => {
        if (e.keyCode === 13) {
            e.preventDefault();
        }
    });
});




// Categories Titles
const identityTitle = document.querySelector('#identity');
const coordonnesTitle = document.querySelector('#coordonnees');
const courseTitle = document.querySelector('#course');
const categoryTitle = document.querySelector('#course-category');
const datetimeTitle = document.querySelector('#datetime');
const moreInfosTitle = document.querySelector('#more-infos');


// Message to display
const reservationMessage = document.querySelector('.reservation-message');


// Confirmation button
const sendButton = document.querySelector('#send-button');
// Estimation Button
const estimateButton = document.querySelector('#estimate-button');



const identity = [customerFirstNameField, customerLastNameField];
let firstNameFilled = false;
let lastNameFilled = false;

identity.forEach((field) => {
    field.addEventListener('input', (e) => {
        const value = e.target.value;
        if (field === customerFirstNameField) {
            firstNameFilled = value.length > 1;
        } else if (field === customerLastNameField) {
            lastNameFilled = value.length > 1;
        }

        if (firstNameFilled && lastNameFilled) {
            identityTitle.innerHTML = 'Identité <i class="bi bi-check-circle"></i>';
        } else {
            identityTitle.innerHTML = 'Identité';
        }
    });
});


const coordonees = [phoneField, customerEmailField];

let coordoneesFilled = false;

let phoneFilled = false;
let emailFilled = false;

coordonees.forEach((field) => {
    field.addEventListener('input', (e) => {
        const value = e.target.value;
        if (field === phoneField) {
            const validPhone = isValidPhoneNumber(value);

            if (validPhone) {
                phoneFilled = true;
            } else {
                phoneFilled = false;
            }

        } else if (field === customerEmailField) {
            const validEmail = isValidEmail(value);

            if (validEmail) {
                emailFilled = true;
            } else {
                emailFilled = false;
            }
        }

        if (phoneFilled && emailFilled) {
            coordonnesTitle.innerHTML = 'Coordonnées <i class="bi bi-check-circle"></i>';
            coordoneesFilled = true;
        } else {
            coordonnesTitle.innerHTML = 'Coordonnées';
            coordoneesFilled = false;
        }
    });
});


let courseGrade = "standard";


const courseGradeField = document.querySelectorAll('.form-check-input');

courseGradeField.forEach((field) => {
    field.addEventListener('change', (e) => {
        if (field.checked) {
            courseGrade = field.id;
            categoryTitle.innerHTML = 'Catégorie <i class="bi bi-check-circle"></i>';
        } else {
            courseGrade = false;
        }
    })
});


const datetime = [happeningDateField, happeningTimeField];

let happeningDateFilled = false;
let happeningTimeFilled = false;


happeningDateField.addEventListener('change', (e) => {
    const value = e.target.value;
    const valid = isValidDateFormat(value);

    if (valid) {
        happeningDateFilled = true;
    } else {
        happeningDateFilled = false;
    }
});

happeningTimeField.addEventListener('input', (e) => {
    const value = e.target.value;

    const valid = isValidTimeFormat(value);

    if (valid) {
        happeningTimeFilled = true;
    } else {
        happeningTimeFilled = false;
    }

    if (happeningDateFilled && happeningTimeFilled) {
        datetimeTitle.innerHTML = 'Date et Heure <i class="bi bi-check-circle"></i>';
    } else {
        datetimeTitle.innerHTML = 'Date et Heure';
    }

});



passengersField.addEventListener('change', (e) => {
    const value = e.target.value;
    if (value !== "") {
        moreInfosTitle.innerHTML = 'Informations Complémentaires <i class="bi bi-check-circle"></i>';
    } else {
        moreInfosTitle.innerHTML = 'Informations Complémentaires';
    }
});


// TRANSFORM DATE FIELD INTO FLATPICKR WITH TODAY'S DATE
makeFlatPickr(happeningDateField, "today");



// Allowing only numbers or +33 in phone input
phoneField.addEventListener('input', (e) => {
    const phoneNumber = e.target.value;

    controlPhoneInput(e, phoneNumber);
});


// Enforcing inputs for passengers field
passengersField.addEventListener('input', (e) => {
    const value = e.target.value;

    if (value < 1) {
        e.target.value = 1;
    } else if (value > 8) {
        e.target.value = 8;
    }
});


// Enforcing cases inputs
[bigCases, smallCases].forEach((field) => {
    field.addEventListener('input', (e) => {
        const value = e.target.value;

        if (value < 0) {
            e.target.value = 0;
        } else if (value > 5) {
            e.target.value = 5;
        } else if (value === ".") {
            e.target.value = 0;
        }
    });
});


let lastEstimation = {
    'origin': '',
    'destination': '',
    'courseGrade': '',
};


[sendButton, estimateButton].forEach((button) => {

    // Check if all mandatory fields are filled
    button.addEventListener('click', (e) => {
        e.preventDefault();

        const valid = checkRequiredFields(Array.from(mandatoryInputs));

        if (valid.length > 0) {
            valid.forEach((field) => {
                field.style.background = '#0366C0';

                setTimeout(() => {
                    field.style.background = 'white';
                    field.style.color = 'black';
                }, 3000);
            });

            showMessage('error', 'Veuillez remplir les champs nécessaires');
        } else {

            if (!coordoneesFilled) {
                showMessage('error', 'Veuillez entrer un numéro de téléphone et une adresse email.');
                return;
            }

            if (button === sendButton) {
                const csrfToken = Cookies.get('csrftoken');
                const url = '/api/reservation/create/';

                const formData = new FormData();

                formData.append('customer_first_name', customerFirstNameField.value);
                formData.append('customer_last_name', customerLastNameField.value);
                formData.append('customer_email', customerEmailField.value);
                formData.append('customer_phone_number', phoneField.value);
                formData.append('pickup_address', pickupAddressField.value);
                formData.append('destination', destinationField.value);
                formData.append('happening_date', happeningDateField.value);
                formData.append('happening_time', happeningTimeField.value);
                formData.append('passengers', passengersField.value);
                formData.append('course_grade', courseGrade);
                formData.append('small_cases', smallCases.value);
                formData.append('big_cases', bigCases.value);
                formData.append('payment_mode', paymentModeField.value);
                formData.append('comments', moreInfosField.value);

                createCourse(formData, csrfToken, url)
                    .then((response) => {
                        if (response.ok) {
                            showMessage('success', 'Votre demande a bien été prise en compte, un email de confirmation vous sera adressé dans les plus brefs délais.', 10000);
                            // Empty all fields
                            mandatoryInputs.forEach((field) => {
                                field.value = '';
                            });
                            customerEmailField.value = '';
                            phoneField.value = '';

                            setTimeout(() => {
                                window.location.href = '/';
                            }, 10000);


                        } else {
                            console.log(response);
                            showMessage('error', 'Une erreur est survenue, veuillez réessayer plus tard', 8000);
                        }
                    })
            } else if (button === estimateButton) {

                // NECCESSARY DATA TO ESTIMATE PRICE
                const data = {
                    'origin': pickupAddressField.value,
                    'destination': destinationField.value,
                    'courseGrade': courseGrade,
                }

                // Check if data has changed

                if (data.origin !== lastEstimation.origin || data.destination !== lastEstimation.destination || data.courseGrade !== lastEstimation.courseGrade) {
                    estimateCoursePrice(data)
                        .then((response) => {
                            if (response.ok) {
                                response.json().then((data) => {

                                    reservationMessage.innerHTML = `
                                <li>Prix estimé : ${data.price} €</li>
                                <li>Distance : ${data.distance_str}</li>
                                <li>Durée : ${data.duration}</li>`;
                                });
                            } else if (response.status === 403) {
                                showMessage('error', 'Limite de demande atteinte, veuillez réessayer plus tard');
                            }
                        }).catch((error) => {
                            showMessage('error', 'Une erreur est survenue, veuillez réessayer plus tard');
                            throw new Error(error);
                        });
                } 
                lastEstimation = data;
            }
        }
    })
});


// Google Maps Autocomplete


// Identifying inputs to autocomplete
const pickupAddressInput = document.querySelector('#id_pickup_address');
const destinationInput = document.querySelector('#id_destination');

// Creating autocomplete objects
let autoCompletePickupAddress;
let autoCompleteDestination;

// Initializing autocomplete
function initAutocomplete() {
    autoCompletePickupAddress = new google.maps.places.Autocomplete(pickupAddressInput, options);
    autoCompleteDestination = new google.maps.places.Autocomplete(destinationInput, options);

}