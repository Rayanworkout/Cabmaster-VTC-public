
// ALLOWING THE WORKER TO MODIFY A COURSE

// STORING LAST VALUES SO REQUEST IS NOT SENT IF VALUES ARE THE SAME
let lastCustomerLastName = "";
let lastDate = "";
let lastTime = "";
let lastPickupAddress = "";
let lastDestination = "";

const courses = document.querySelector('#courses');


// Get all rows in the table body
const rows = courses.getElementsByTagName('tr');
// LOOP TO MAKE ALL ROWS OF PENDING COURSES CLICKABLE
for (let i = 0; i < rows.length; i++) {
    // Making the whole row clickable
    // Make clickable courses that are not cancelled

    const statusCell = rows[i].querySelectorAll('td')[6];
    const status = statusCell.textContent.trim();

    if (status !== 'Annulée' && status !== 'Effectuée') {
        rows[i].addEventListener('click', (event) => {
            const cells = event.currentTarget.getElementsByTagName('td');
            // Only values the worker can modify
            const slicedCells = Array.from(cells).slice(0, 6);
            const rowData = [];

            // Getting text content of each cell
            for (let j = 0; j < slicedCells.length; j++) {
                const cellData = slicedCells[j].textContent
                rowData.push(cellData)
            }


            const modalTitle = document.querySelector('#modalTitle');
            modalTitle.textContent = rowData[0];

            const customerLastName = document.querySelector('#customer-last-name-edit');
            customerLastName.value = rowData[1];

            const dateField = document.querySelector('#course-date');
            dateField.value = rowData[2];

            // TRANSFORM DATE FIELD INTO FLATPICKR, WITHOUT TODAY'S DATE
            makeFlatPickr(dateField, dateField.value);


            const hourField = document.querySelector('#course-time');
            hourField.value = rowData[3];

            const pickupAddress = document.querySelector('#course-pickup-address');
            pickupAddress.value = rowData[4];

            const destination = document.querySelector('#course-destination');
            destination.value = rowData[5];

            // Showing the modal with the data
            $('#modifModal').modal('show');

            lastCustomerLastName = rowData[1];
            lastDate = rowData[2];
            lastTime = rowData[3];
            lastPickupAddress = rowData[4];
            lastDestination = rowData[5];
        })

    }

}


// MODIFY A COURSE

const validateButton = document.querySelector('#validate');

const cancelButton = document.querySelector('#cancel');


// Validate button for course modification
validateButton.addEventListener('click', () => {

    const courseId = document.querySelector('#modalTitle');

    const customerLastName = document.querySelector('#customer-last-name-edit');

    const dateField = document.querySelector('#course-date');
    const hourField = document.querySelector('#course-time');
    const pickupAddress = document.querySelector('#course-pickup-address');
    const destination = document.querySelector('#course-destination');


    const data = {
        'id': courseId.textContent,
        'customer_last_name': customerLastName.value,
        'date': dateField.value,
        'time': hourField.value,
        'pickup_address': pickupAddress.value,
        'destination': destination.value
    }


    // Checking if the values have changed
    if (data['customer_last_name'] === lastCustomerLastName &&
        data['date'] === lastDate &&
        data['time'] === lastTime &&
        data['pickup_address'] === lastPickupAddress &&
        data['destination'] === lastDestination) {

        $('#modifModal').modal('hide');
        return;
    }

    // Validating the date format
    if (!isValidDateFormat(data['date'])) {
        showMessage('error', 'Format de la date incorrect (DD/MM/YYYY)');
        return;

    }

    // Validating the time format
    if (!isValidTimeFormat(data['time'])) {
        showMessage('error', 'Format de l\'heure incorrect (HH:MM)');
        return;
    }

    const csrftoken = Cookies.get('csrftoken');

    updateCourse(data, csrftoken)
        .then((response) => {
            if (response.ok) {
                showMessage('success', 'Course modifiée avec succès.');
                setTimeout(() => {
                    window.location.reload();
                }, 2000); // 3 seconds
            } else {
                throw new Error('Something went wrong');
            }
        })
        .catch((error) => {
            console.error('Error in updateCourse:', error);

        })
});


// Cancel button
cancelButton.addEventListener('click', () => {

    // CONFIRM AND ASK FOR REASON FIRST
    Swal.fire({
        title: "Merci de préciser la raison de l'annulation",
        input: "select",
        confirmButtonColor: '#0c4d8a',
        inputOptions: {
            "non_necessary": "Déplacement plus nécessaire",
            "customer_cancellation": "Initiative du Client",
            "other": "Autre"
        },
        showCancelButton: true,
        inputValidator: (value) => {
            if (!value) {
                return "Merci de préciser une raison";
            }
        }
    }).then((result) => {
        if (result.isConfirmed) {
            selectedValue = result.value;

            const courseId = document.querySelector('#modalTitle');

            const data = {
                "id": courseId.textContent,
                "reason": selectedValue
            }


            const csrftoken = Cookies.get('csrftoken');
            cancelCourse(data, csrftoken)
                .then((response) => {
                    if (response.ok) {
                        showMessage('success', 'Course annulée.');
                        setTimeout(() => {
                            window.location.reload();
                        }, 2000); // 3 seconds
                    } else {
                        throw new Error('Something went wrong');
                    }
                })
        }
    });
});
// ADDING A NEW COURSE

const addCourseButton = document.querySelector('#add-button');
const closeModalButton = document.querySelector('#abort');


const createButton = document.querySelector('#create-course');



// Showing and hiding a map as modal background
const map = document.querySelector('.map-worker');
const mainContent = document.querySelector('.main-content');

const modals = [document.querySelector('#add-course-modal'), document.querySelector('#modifModal')];

modals.forEach((modal) => {
    modal.addEventListener('show.bs.modal', () => {
        // Hiding the map
        map.style.display = 'block';
        mainContent.style.display = 'none';
    });

    modal.addEventListener('hide.bs.modal', () => {
        // Showing the map
        map.style.display = 'none';
        mainContent.style.display = 'block';
    })
});




addCourseButton.addEventListener('click', () => {
    $('#add-course-modal').modal('show');

    // Closing the modal
    closeModalButton.addEventListener('click', () => {
        $('#add-course-modal').modal('hide');
    });


    const customerFirstName = document.querySelector('#id_customer_first_name');
    const customerLastName = document.querySelector('#id_customer_last_name');
    const customerPhone = document.querySelector('#id_customer_phone_number');
    const pickupAddress = document.querySelector('#id_pickup_address');
    const destination = document.querySelector('#id_destination');
    const passengers = document.querySelector('#passengers');
    const courseGrade = document.querySelector('#id_course_grade');
    const happeningTime = document.querySelector('#id_happening_time');
    const smallCases = document.querySelector('#small-cases');
    const bigCases = document.querySelector('#big-cases');


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


    // Allowing only numbers or +33 in phone input
    customerPhone.addEventListener('input', (e) => {
        const phoneNumber = e.target.value;

        controlPhoneInput(e, phoneNumber);
    });


    // Enforcing inputs for passengers field
    passengers.addEventListener('input', (e) => {
        const value = e.target.value;

        if (value < 0) {
            e.target.value = 0;
        } else if (value > 8) {
            e.target.value = 8;
        }
    });



    // TRANSFORM DATE FIELD INTO FLATPICKR WITH TODAY'S DATE
    const dateField = document.querySelector('#id_happening_date');
    makeFlatPickr(dateField, "today");

    createButton.addEventListener('click', () => {
        const data = {
            'customer_first_name': customerFirstName.value,
            'customer_last_name': customerLastName.value,
            'customer_email': document.querySelector('#id_customer_email').value,
            'customer_phone_number': customerPhone.value,
            'pickup_address': pickupAddress.value,
            'destination': destination.value,
            'happening_date': dateField.value,
            'happening_time': happeningTime.value,
            'passengers': passengers.value,
            'course_grade': courseGrade.value,
            'small_cases': smallCases.value,
            'big_cases': bigCases.value,
            'payment_mode': document.querySelector('#id_payment_mode').value,
            'more_infos': document.querySelector('#id_more_infos').value,
        }

        // Validating the date format
        if (!isValidDateFormat(data['happening_date'])) {
            showMessage('error', 'Format Incorrect (DD/MM/YYYY)');
            return;

        }

        // Validating the time format
        if (!isValidTimeFormat(data['happening_time'])) {
            showMessage('error', 'Format Incorrect (HH:MM)');
            return;
        }

        // Checking if all necessary fields are filled

        const valid = checkRequiredFields(
            [
                customerFirstName,
                customerLastName,
                customerPhone,
                pickupAddress,
                destination,
                courseGrade,
                passengers,
                smallCases,
                bigCases,
            ]
        );

        if (valid.length > 0) {
            showMessage('error', 'Veuillez remplir tous les champs obligatoires');
            highlightFields(
                valid,
            )
            return;
        }

        // SENDING THE DATA TO THE SERVER
        const csrftoken = Cookies.get('csrftoken');
        const url = '/api/reservation/create/';

        createCourse(data, csrftoken, url)
            .then((response) => {
                if (response.ok) {
                    showMessage('success', 'Course ajoutée avec succès.');
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000); // 2 seconds
                } else {
                    console.error('Error in createCourse:', error);
                    throw new Error('Something went wrong');
                }
            });
    }
    )
});

// ESTIMATE PRICE BUTTON

const estimateButton = document.querySelector('#estimate-course');

estimateButton.addEventListener('click', () => {

    const pickupAddress = document.querySelector('#id_pickup_address');
    const destination = document.querySelector('#id_destination');
    const courseGrade = document.querySelector('#id_course_grade');

    // NECCESSARY DATA TO ESTIMATE PRICE
    const data = {
        'origin': pickupAddress.value,
        'destination': destination.value,
        'courseGrade': courseGrade.value,
    }

    // Checking if all necessary fields are filled

    const valid = checkRequiredFields(
        [
            pickupAddress,
            destination,
            courseGrade
        ],
    );

    if (valid.length > 0) {
        showMessage('error', 'Veuillez remplir les champs nécessaires pour estimer le prix');
        highlightFields(
            valid,
        )
        return;
    }

    // IF EVERYTHING IS OK, ESTIMATE THE PRICE
    const estimateMessageLines = document.querySelectorAll('.estimation-data');

    estimateCoursePrice(data)
        .then((response) => {
            if (response.ok) {
                response.json().then((data) => {
                    estimateMessageLines[0].textContent = `Prix estimé : ${data.price} €`;
                    estimateMessageLines[1].textContent = `Distance : ${data.distance_str}`;
                    estimateMessageLines[2].textContent = `Durée : ${data.duration}`;
                });

            } else {
                showMessage('error', 'Une erreur est survenue, rééssayez plus tard.');
            }

        })
}
);



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
