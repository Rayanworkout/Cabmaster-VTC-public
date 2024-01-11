import os
import re
from datetime import datetime

import requests
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from weasyprint import HTML

# from cabmaster.celery import app

from .models import BondeReservation, Invoice


def verify_date_time_format(date_str, time_str):
    """Function to check if the date and time are in the correct format"""
    try:
        # Verify the date format
        datetime.strptime(date_str, "%d/%m/%Y")

        # Verify the time format
        datetime.strptime(time_str, "%H:%M")

        return True

    except ValueError:
        return False


def convert_to_datetime(date_string):
    """Function to convert a string to a datetime object"""

    date_format = "%d/%m/%Y %H:%M"

    try:
        datetime_obj = datetime.strptime(date_string, date_format)
        return datetime_obj

    except ValueError:
        return None


def telegram_message(message):
    requests.get(
        "https://api.telegram.org/bot:TOKEN/"
        "sendMessage?chat_id=CHAT_ID&text={}".format(message)
    )

def get_date():
    """Function to get the current date"""
    return datetime.now().strftime("%d/%m/%Y")


def get_time():
    """Function to get the current time"""
    return datetime.now().strftime("%H:%M")


def get_distance(origin, destination):
    """Function to get the distance between two addresses"""
    # Price: 0.005€ per request
    # 100$ = 20 000 requests, 666 requests per day
    
    # For testing purposes
    
    # if origin == "bad_origin":
    #     raise ValidationError("Invalid address")
    
    # return {
    #     "distance_meters": 8500,
    #     "distance_str": "8.5 km",
    #     "duration": "20 minutes",
    #     "origin": "test address",
    #     "destination": "test address destiantion",
    # }

    API_KEY = "KEY"

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}"

    r = requests.get(url).json()

    try:
        distance_meters = r["routes"][0]["legs"][0]["distance"]["value"]
        distance_str = r["routes"][0]["legs"][0]["distance"]["text"]
        duration = r["routes"][0]["legs"][0]["duration"]["text"]
        response_origin = r["routes"][0]["legs"][0]["start_address"]
        response_destination = r["routes"][0]["legs"][0]["end_address"]

        return {
            "distance_meters": distance_meters,
            "distance_str": distance_str,
            "duration": duration,
            "origin": response_origin,
            "destination": response_destination,
        }
    
    except (KeyError, IndexError):
        raise ValidationError("Invalid address")


def calculate_price(origin, destination, grade):
    """Function to calculate the price of a ride
    depending on the grade and the distance
    Cabmaster takes a 20% commission on each ride"""

    distance_obj = get_distance(origin, destination)

    distance_meters = distance_obj["distance_meters"]
    distance_str = distance_obj["distance_str"]
    duration = distance_obj["duration"]
    response_origin = distance_obj["origin"]
    response_destination = distance_obj["destination"]

    distance_km = distance_meters / 1000

    if grade == "standard":
        if distance_km <= 5:
            price = 25

        elif 5 < distance_km <= 10:
            price = 30

        elif 10 < distance_km <= 60:
            price = distance_km * 2.8

        elif distance_km > 60:
            price = distance_km * 2.5

    elif grade == "berline":
        if distance_km <= 15:
            price = 50

        elif 15 < distance_km <= 25:
            price = distance_km * 3.5

        elif 25 < distance_km <= 40:
            price = distance_km * 2.8

        elif distance_km > 40:
            price = distance_km * 2.6

    elif grade == "van":
        if distance_km <= 15:
            price = 75

        elif 15 < distance_km <= 30:
            price = distance_km * 5

        elif distance_km > 30:
            price = distance_km * 3

    else:
        raise ValidationError("Invalid grade")
    
    return {
        "price": int(round(price)),
        "distance_str": distance_str,
        "duration": duration,
        "origin": response_origin,
        "destination": response_destination,
    }

# @app.task
def custom_send_email_contact(
    name,
    subject,
    message,
    contacts,
    recipients_list,
):
    """Custom function to send email after a contact form submission
    It can be a Celery task in order to send the email asynchronously and
    direclty return a response to the user"""
    try:
        # Send email to the customer
        html_message = render_to_string(
            f"home/email/email_contact.html", {"name": name}
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Équipe Cabmaster",
            message=plain_message,
            recipient_list=recipients_list,
            html_message=html_message,
            from_email="Contact@cabmaster.fr",
        )

        # And then send email to the admin
        html_message_admin = render_to_string(
            f"home/email/email_contact_admin.html",
            {
                "name": name,
                "subject": subject,
                "message": message,
                "contacts": contacts,
            },
        )

        plain_message_admin = strip_tags(html_message_admin)

        send_mail(
            subject="Demande de contact",
            message=plain_message_admin,
            recipient_list=["contact.cabmaster@gmail.com"],
            html_message=html_message_admin,
            from_email="Contact@cabmaster.fr",
        )
        
        return "Contact email sent successfully"

    except Exception as e:
        telegram_message(f"Could not send contact email to {name}: {e}")

        raise ValidationError(f"Could not send contact email: {e}")
        
# @app.task
def custom_send_email_reservation(
    name,
    pickup_address,
    destination,
    wanted_date,
    wanted_time,
    passengers,
    course_price,
    course_grade,
    payment_mode,
    small_cases,
    big_cases,
    comments,
    customer_phone_number,
    recipients_list,
):
    """Custom function to send email after a reservation form submission
    It can a Celery task in order to send the email asynchronously and
    direclty return a response to the user"""
    try:
        # Send email to the customer
        html_message = render_to_string(
            f"home/email/email_reservation.html",
            {
                "name": name,
                "customer_phone_number": customer_phone_number,
                "pickup_address": pickup_address,
                "destination": destination,
                "wanted_date": wanted_date,
                "wanted_time": wanted_time,
                "passengers": passengers,
                "course_price": course_price,
                "payment_mode": payment_mode,
                "course_grade": course_grade,
                "small_cases": small_cases,
                "big_cases": big_cases,
                "comments": comments,
            },
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Réservation Confirmée",
            message=plain_message,
            recipient_list=recipients_list,
            html_message=html_message,
            from_email="contact.cabmaster@gmail.com",
        )
        
        return "Reservation email sent successfully"

    except Exception as e:
        telegram_message(f"Could not send reservation email to {name}: {e}")

        raise ValidationError(f"Could not send reservation email: {e}")

def generate_invoice(course):
    """Generate an invoice for a course"""

    now = datetime.now().strftime("%d/%m/%Y")

    course_price = course.course_price

    tva = course_price * 0.2
    ht_price = course_price * 0.8

    invoice = Invoice(
        course=course,
        customer=course.customer,
        ht_price=ht_price,
        ttc_price=course.course_price,
        payment_method=course.payment_mode,
    )

    invoice.save()

    # Get  HTML template
    template = get_template("home/invoice_template.html")
    context = {
        "course": course,
        "invoice_date": now,
        "ht_price": int(round(ht_price)),
        "tva": int(round(tva)),
    }

    # Render the HTML template with your context data
    html_string = template.render(context)

    # Create a WeasyPrint HTML object
    html = HTML(string=html_string)

    # Generate the PDF
    pdf_file = html.write_pdf()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the file
    file_path = os.path.join(
        current_dir, f"../home/templates/home/archives/facture_{course.id}.pdf"
    )

    # Save the PDF to the server
    with open(file_path, "wb") as pdf_output:
        pdf_output.write(pdf_file)

    # Create an HTTP response with the PDF content
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f'attachement; filename="facture_{course.customer.last_name}_course_{course.id}.pdf"'

    return response


def generate_bon_reservation(course):
    now = datetime.now().strftime("%d/%m/%Y")

    bon_reservation = BondeReservation(
        course=course,
    )
    bon_reservation.save()

    # Get your HTML template
    template = get_template("home/br_template.html")
    context = {
        "course": course,
        "date": now,
    }

    # Render the HTML template with your context data
    html_string = template.render(context)

    # Create a WeasyPrint HTML object
    html = HTML(string=html_string)

    # Generate the PDF
    pdf_file = html.write_pdf()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the file
    file_path = os.path.join(
        current_dir, f"../home/templates/home/archives/br_{course.id}.pdf"
    )

    # Save the PDF to the server
    with open(file_path, "wb") as pdf_output:
        pdf_output.write(pdf_file)

    # Create an HTTP response with the PDF content
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachement; filename="br_{course.id}.pdf"'

    return response


def is_valid_email(email):
    email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return bool(re.match(email_regex, email))


def is_valid_phone_number(phone_number):
    # Regular expression pattern for French phone numbers
    french_phone_regex = r"^(\+33|0)(6|7)\d{8}$"

    # Check if the cleaned number matches the pattern
    is_valid = bool(re.match(french_phone_regex, phone_number))

    return is_valid


def clean_reservation_form_data(data):
    """Function to clean the data from the reservation form
    and making some calculations"""
    data = data.copy()

    # Validating phone number
    phone_number = data.get("customer_phone_number")
    if not is_valid_phone_number(phone_number):
        raise ValidationError("Invalid phone number")
    
    # and email
    if not is_valid_email(data.get("customer_email")):
        raise ValidationError("invalid email")
    
    # Validating passengers value
    try:
        int(data.get("passengers"))
    except ValueError:
        raise ValidationError("Invalid passengers value")

    # COURSE
    pickup_address = data.get("pickup_address")
    destination = data.get("destination")
    course_grade = data.get("course_grade")

    # WE CALCULATE THE COURSE PRICE
    calculation = calculate_price(pickup_address, destination, course_grade)

    course_price = calculation["price"]
    data["course_price"] = course_price

    # Cabmaster commission
    data["cabmaster_commission"] = round(course_price * 0.2, 2)

    payment_mode = data.get("payment_mode")

    # We make the payment mode human readable
    data["payment_mode"] = (
        "Espèces"
        if payment_mode == "cash"
        else "Carte Bancaire"
        if payment_mode == "card"
        else "En Ligne"
        if payment_mode == "online"
        else "Non renseigné"
    )

    course_date = data.get("happening_date")
    course_time = data.get("happening_time")

    # We combine date string and time string to make a datetime object
    data["course_datetime"] = convert_to_datetime(f"{course_date} {course_time}")

    # We test if there is some comments in the comment field
    try:
        data["comments"]
        if data["comments"] == "":
            data["comments"] = "Aucun"
        else:
            data["comments"] = data["comments"]
    except KeyError:
        data["comments"] = "Aucun"

    return data