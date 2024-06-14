import json

from courses.models import Course
from customers.models import Customer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from home.utils import convert_to_datetime, telegram_message
from workers.models import Worker
from django.shortcuts import get_object_or_404


@ratelimit(key='user_or_ip', rate='10/m')
@login_required(login_url="login")
def update_course(request):
    """Endpoint to update or change status of a course from the worker dashboard"""
    if request.method == "PUT":
        try:
            data = json.loads(request.body)

            course_id = data["id"]
            customer_last_name = data["customer_last_name"]
            course_date = data["date"]
            course_time = data["time"]
            course_pickup_address = data["pickup_address"]
            course_destination = data["destination"]

            course_instance = get_object_or_404(Course, id=course_id)
            
            customer_instance = get_object_or_404(Customer, id=course_instance.customer.id)

            worker = get_object_or_404(Worker, id=request.user.worker.id)
            
            if course_instance.worker == worker:
                course_instance.happening_datetime = convert_to_datetime(
                    f"{course_date} {course_time}"
                )

                course_instance.pickup_address = course_pickup_address
                course_instance.destination = course_destination

                course_instance.save()

                customer_instance.last_name = customer_last_name
                customer_instance.save()

                return JsonResponse(
                    {"message": "Course updated successfully"}, status=204
                )

            else:
                return JsonResponse({"error": "Bad Request"}, status=403)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    else:
        return JsonResponse({"error": "Bad Request"}, status=400)



@login_required(login_url="login")
@ratelimit(key='user_or_ip', rate='10/m')
def cancel_course(request):
    """Endpoint to cancel a course from the worker dashboard"""
    if request.method == "PUT":
        try:
            data = json.loads(request.body)

            course_id = data["id"]
            # Extracting cancel reason from the request body
            try:
                data["reason"]
            except KeyError:
                return JsonResponse({"error": "Please provide a reason"}, status=400)

            course_instance = Course.objects.get(id=course_id)
            worker = Worker.objects.get(id=request.user.worker.id)

            if course_instance.worker == worker:
                course_instance.status = "cancelled"
                course_instance.save()

                telegram_message(
                    f"Course {course_id} cancelled by {worker}\n\nReason: {data['reason']}"
                )

                return JsonResponse(
                    {"message": "Course cancelled successfully"}, status=204
                )

            else:
                return JsonResponse({"error": "Bad Request"}, status=403)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    else:
        return JsonResponse({"error": "Bad Request"}, status=400)