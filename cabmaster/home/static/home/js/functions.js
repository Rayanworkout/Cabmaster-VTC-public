
// FILE WITH ALL USEFUL FUNCTIONS THAT ARE SHARED ACROSS THE APPLICATION


// Showing which page is active in the navigation bar
const currentPath = window.location.pathname;


// Get all the navigation links
const navLinks = document.querySelectorAll('.active-item > a');

// Loop through each link and check if it matches the current path
navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.style.borderBottom = '2px solid #fff';
    }
});



// Function to check if the email is i nthe correct format
function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}


// Function to check if the phone number is in the correct format
function isValidPhoneNumber(phoneNumber) {
    // Regular expression pattern for French phone numbers
    const frenchPhoneRegex = /^(\+33|0)(6|7)\d{8}$/;

    // Check if the cleaned number matches the pattern
    const isValid = frenchPhoneRegex.test(phoneNumber);

    return isValid;
}


function controlPhoneInput(e, phoneNumber) {
    if (/[^+\d]/.test(phoneNumber)) {
        e.target.value = phoneNumber.replace(/[^+\d]/g, ''); // Remove all non-digit characters except +
    }

    // Check if the number starts with 33
    // If so, I add + to the beginning of the number
    if (/^33/.test(phoneNumber) && phoneNumber.length > 2) {
        e.target.value = '+' + phoneNumber;
    }
}

// Function to check if the password is strong enough
// and not too similar to the email address
function isStrongPassword(password, email) {
    // Check password length
    if (password.length < 8) {
        return false;
    }

    // Check for lowercase and uppercase letters
    const hasLowercase = /[a-z]/.test(password);
    const hasUppercase = /[A-Z]/.test(password);

    // if (!hasLowercase || !hasUppercase) {
    //     return false;
    // }

    // Check for a symbol (non-alphanumeric character)
    const hasSymbol = /[^a-zA-Z0-9]/.test(password);

    // if (!hasSymbol) {
    //     return false;
    // }

    // Check if the password is not too similar to the email address
    const emailParts = email.split('@')[0];
    if (password.includes(email) || password.includes(emailParts)) {
        return false;
    }

    return true;
}


// FUNCTION TO CHECK IF DATE IS IN THE RIGHT FORMAT
const isValidDateFormat = (dateString) => {
    // Regular expression for DD/MM/YYYY format
    const dateRegex = /^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/202[3-9]|20[3-9][0-9]$/;

    return dateRegex.test(dateString);
}


const isValidTimeFormat = (timeString) => {
    // Regular expression for HH:MM format (24-hour format)
    const timeRegex = /^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/;

    return timeRegex.test(timeString);
}



let lastInput = "";
// FUNCTION TO CHECK IF A FIELD IS IN THE RIGHT FORMAT USING A DEBOUNCER
const debounceInput = (fieldValue, errorDiv, errorMessage, validator, callback) => {
    clearTimeout(fieldValue.timer);

    fieldValue.timer = setTimeout(() => {
        if (fieldValue.length > 4 && fieldValue !== lastInput) {
            lastInput = fieldValue;
            const valid = validator(fieldValue);

            if (!valid) {
                errorDiv.textContent = errorMessage;
                callback(false); // Callback with false if validation fails
            } else {
                errorDiv.textContent = "";
                callback(true); // Callback with true if validation succeeds
            }
        }
    }, 500);
};



const loginUser = async (formData, csrfToken) => {
    try {

        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        });

        const data = await response.json();

        if (data.success === true) {
            if ('next' in data) {
                return { 'success': true, 'next': data.next };
            } else {
                return { 'success': true };
            }

        } else if (data.success === false) {
            return { 'success': false };
        }
    } catch (error) {
        console.error('Error:', error);
        // Handle the error or return a specific value indicating failure
        return { 'success': false };
    }
};


const postForm = async (url, formData) => {
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success === true) {
            return { 'success': true };

        } else if (data.success === false) {
            return { 'success': false };
        }

    } catch (error) {
        console.log(error);
    }
};


const showMessage = (type, message, timer=4000) => {
    Swal.fire({
        text: message,
        timer: timer,
        toast: true,
        confirmButtonColor: '#0c4d8a',
        timerProgressBar: true,
        icon: type,
    });
}



// FUNCTION THAT ENABLE A WORKER TO MODIFY A COURSE
const updateCourse = async (data, csrftoken) => {
    try {
        // I get modifUrl from the template
        // Because I use django template tags to get the url

        // Sending the data to the server
        const response = await fetch('/partenaires/api/update/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(data)
        });
        return response;

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
};


// FUNCTION THAT ENABLE A WORKER TO CANCEL A COURSE
const cancelCourse = async (data, csrftoken) => {
    try {

        // Sending the data to the server
        const response = await fetch("/partenaires/api/cancel/", {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(data)
        });
        return response;

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
};


// FUNCTION THAT ENABLE A WORKER TO CREATE A COURSE
const createCourse = async (formData, csrftoken, url) => {
    try {
        // Sending the data to the server
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData
            
        });
        return response;

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}


// FUNCTION TO CHECK IF REQUIRED FIELDS ARE FILLED
// AND RETURN AN ARRAY OF THE EMPTY FIELDS
const checkRequiredFields = (fields) => {
    let errors = [];

    fields.forEach(field => {
        if (field.value === "") {
            errors.push(field);
        }
    });

    return errors;
}



// Function to highlight the required fields
const highlightFields = (fields) => {
    fields.forEach(field => {
        field.style.border = "1px solid rgb(236, 34, 68)";

        setTimeout(() => {
            field.style.border = "none";
        }, 3000)
    });
};



// Function to transform date input into a FlatPickr object
const makeFlatPickr = (element, defaultDate = null) => {
    flatpickr(element, {
        dateFormat: "d/m/Y",
        minDate: "today",
        defaultDate: defaultDate,
    });
}


// Function to estimate the price of a course
// By sending a request to the server

const estimateCoursePrice = async (data) => {
    try {
        const origin = data.origin;
        const destination = data.destination;
        const courseGrade = data.courseGrade;

        const url = `/api/estimate/${origin}/${destination}/${courseGrade}`;

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        return response;

    } catch (error) {
        console.error('There was a problem with the price estimation operation:', error);
        throw error;
    }
};



// GOOGLE PLACES AUTOCOMPLETE
// Price: 0.00283€ per request
// 100$ = 35 000 requests per month, 1160 requests per day
// Creating custom bounds
const center = { lat: 43.298955618741616, lng: 5.3698729058167265 };


// Create a bounding box
// +5 = 500km
const defaultBounds = {
    north: center.lat + 5,
    south: center.lat - 5,
    east: center.lng + 5,
    west: center.lng - 5,
};

// Creating options for autocomplete
const options = {
    bounds: defaultBounds,
    types: ['geocode', 'establishment'],
    componentRestrictions: { 'country': ['fr'] },
    fields: ['name'],
    strictBounds: true,
}
