import json

from courses.models import Course
from customers.models import Customer
from django.contrib.auth.decorators import login_required

# Importing exceptions
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from .utils import (
    calculate_price,
    clean_reservation_form_data,
    custom_send_email_reservation,
    custom_send_email_contact,
    generate_bon_reservation,
    generate_invoice,
    telegram_message,
)

from workers.models import Worker

from .forms import ContactForm


@ratelimit(key="user_or_ip", rate="5/m")
def reserve_course(request):
    """Endpoint to create a course from the reservation page
    or worker dashboard"""
    if request.method == "POST":
        # We first clean the data using function from utils.py
        try:
            cleaned_data = clean_reservation_form_data(request.POST)

            customer_email = cleaned_data["customer_email"]
            course_price = cleaned_data["course_price"]

            course_date = request.POST["happening_date"]
            course_time = request.POST["happening_time"]

        except ValidationError as e:
            return JsonResponse(
                {"error": "ValidationError", "message": str(e)}, status=400
            )

        except (KeyError, json.JSONDecodeError):
            return JsonResponse(
                {"error": "Invalid JSON data", "message": str(e)}, status=400
            )

        except TypeError as e:
            return JsonResponse({"error": "TypeError", "message": str(e)}, status=400)

        # CREATING A CUSTOMER INSTANCE IF THE CUSTOMER DOESN'T EXIST YET
        customer_exists = Customer.objects.filter(email=customer_email).exists()

        try:
            if not customer_exists:
                customer_instance = Customer.objects.create(
                    first_name=cleaned_data["customer_first_name"],
                    last_name=cleaned_data["customer_last_name"],
                    email=customer_email,
                    phone_number=cleaned_data["customer_phone_number"],
                )

                customer_instance.save()

                customer_first_name = customer_instance.first_name
                customer_last_name = customer_instance.last_name
                customer_phone_number = customer_instance.phone_number

            elif customer_exists:
                customer_instance = Customer.objects.get(email=customer_email)

                customer_first_name = customer_instance.first_name
                customer_last_name = customer_instance.last_name
                customer_phone_number = customer_instance.phone_number

            # AND ALSO A COURSE INSTANCE
            # FIRST VERIFY IF THIS COURSE HAS BEEN CREATED BY A WORKER
            if request.user.is_authenticated and request.user.user_type == "worker":
                worker = Worker.objects.get(user=request.user)
                # WORKERS TAKE A 5% COMMISSION ON EACH COURSE
                worker_commission = round(int(course_price) * 0.05, 2)
            else:
                worker = None
                worker_commission = 0

            course_instance = Course.objects.create(
                customer=customer_instance,
                course_price=course_price,
                cabmaster_commission=cleaned_data["cabmaster_commission"],
                worker=worker,
                small_cases=cleaned_data["small_cases"],
                big_cases=cleaned_data["big_cases"],
                worker_commission=worker_commission,
                course_grade=cleaned_data["course_grade"],
                happening_datetime=cleaned_data["course_datetime"],
                pickup_address=cleaned_data["pickup_address"],
                destination=cleaned_data["destination"],
                payment_mode=cleaned_data["payment_mode"],
                passengers=cleaned_data["passengers"],
                comments=cleaned_data["comments"],
            )

            course_instance.save()

        except IntegrityError as e:
            # Handle database integrity issues
            return JsonResponse(
                {"error": "Database integrity error", "message": e}, status=400
            )

        except ValidationError as e:
            # Handle validation errors
            return JsonResponse(
                {"error": "Field Validation error", "message": e}, status=400
            )

        except TypeError as e:
            # Handle type-related errors
            return JsonResponse({"error": "TypeError", "message": e}, status=400)

        except ValueError as e:
            # Handle value-related errors
            return JsonResponse({"error": "ValueError", "message": e}, status=400)

        except ObjectDoesNotExist as e:
            # Handle related object does not exist
            return JsonResponse(
                {"error": "Object does not exist error", "message": e}, status=400
            )

        # Sending email to the customer
        try:
            custom_send_email_reservation(
                name=f"{customer_first_name.capitalize()} {customer_last_name.capitalize()}",
                customer_phone_number=customer_phone_number,
                pickup_address=cleaned_data["pickup_address"],
                destination=cleaned_data["destination"],
                wanted_date=course_date,
                wanted_time=course_time,
                passengers=cleaned_data["passengers"],
                course_price=course_price,
                course_grade=cleaned_data["course_grade"],
                payment_mode=cleaned_data["payment_mode"],
                comments=cleaned_data["comments"],
                small_cases=cleaned_data["small_cases"],
                big_cases=cleaned_data["big_cases"],
                recipients_list=[customer_email],
            )

            # And telegram message to the admin
            telegram_message(
                f"Nouvelle Réservation\n\n"
                f"Grade: {cleaned_data['course_grade']}\n\n"
                f"Date: {course_date} à {course_time}\n\n"
                f"Client: {customer_first_name} {customer_last_name}\n\n"
                f"Coordonnées: {customer_phone_number} / {customer_email}\n\n"
                f"Adresse de départ: {cleaned_data['pickup_address']}\n"
                f"Destination: {cleaned_data['destination']}\n\n"
                f"Nombre de passagers: {cleaned_data['passengers']}\n"
                f"Petites valises: {cleaned_data['small_cases']}\n"
                f"Grandes valises: {cleaned_data['big_cases']}\n"
                f"Prix: {course_price}€\n"
                f"Commission Cabmaster: {cleaned_data['cabmaster_commission']}€\n\n"
                f"Commentaires: {cleaned_data['comments']}\n\n"
                f"Mode de paiement: {cleaned_data['payment_mode']}\n\n"
                f"Partenaire: {worker}\n"
            )

            return JsonResponse({"message": "Course created successfully"}, status=201)

        except Exception as e:
            telegram_message(f"Could not send reservation email to {customer_email}")
            return JsonResponse(
                {"error": "error occured when sending confirmation mail", "message": e},
                status=500,
            )

    else:
        # If method is not POST
        return JsonResponse({"error": "Bad Request"}, status=400)


@ratelimit(key="user_or_ip", rate="5/m")
def estimate_price(request, origin, destination, course_grade):
    """Function to estimate the price of a ride"""
    if request.method == "GET":
        try:
            calculation = calculate_price(origin, destination, course_grade)

            price = calculation["price"]
            distance_str = calculation["distance_str"]
            duration = calculation["duration"]

            # We translate the duration
            duration = duration.replace("hours", "heures")
            duration = duration.replace("hour", "heure")
            duration = duration.replace("mins", "minutes")

            return JsonResponse(
                {
                    "price": price,
                    "distance_str": distance_str,
                    "duration": duration,
                },
                status=200,
            )

        except ValidationError as e:
            return JsonResponse({"error": "ValidationError"}, status=400)

        except Exception as e:
            print(e)
            return JsonResponse({"error": "an error occured"}, status=500)

    else:
        return JsonResponse({"error": "Bad Request"}, status=400)


@ratelimit(key="user_or_ip", rate="5/m")
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        # form.is_valid() makes the necessary tests on the data
        if form.is_valid():
            form.save()

            name = form.cleaned_data["name"].capitalize()
            recipient = form.cleaned_data["email"]

            phone = (
                form.cleaned_data["phone_number"]
                if form.cleaned_data["phone_number"]
                else "Non renseigné"
            )

            email = form.cleaned_data["email"]

            # Sending confirmation email to the customer
            custom_send_email_contact(
                name=name,
                subject=form.cleaned_data["subject"],
                message=form.cleaned_data["message"],
                contacts=" / ".join([phone, email]),
                recipients_list=[recipient],
            )

            return JsonResponse({"success": True}, safe=False, status=201)

        else:
            return JsonResponse({"success": False}, safe=False, status=400)

    else:
        return JsonResponse({"message": "Bad Request"}, safe=False, status=400)


@ratelimit(key="user_or_ip", rate="5/m")
@login_required(login_url="login")
def download_invoice(request, pk):
    if request.method == "GET":
        if request.user.is_superuser:
            try:
                course = Course.objects.get(pk=pk)
                if course.status == "done":
                    return generate_invoice(course)
                else:
                    return JsonResponse({"error": "course non validee"}, status=400)

            except ObjectDoesNotExist:
                return JsonResponse({"error": "course does not exist"}, status=400)
        else:
            return JsonResponse({"error": "Unauthorized"}, status=403)

    else:
        return JsonResponse({"error": "Bad Request"}, status=400)


@ratelimit(key="user_or_ip", rate="5/m")
@login_required(login_url="login")
def download_br(request, pk):
    if request.method == "GET":
        if request.user.is_superuser:
            try:
                course = Course.objects.get(pk=pk)
                return generate_bon_reservation(course)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "course does not exist"}, status=400)

        else:
            return JsonResponse({"error": "Unauthorized"}, status=403)

    else:
        return JsonResponse({"error": "Bad Request"}, status=400)
