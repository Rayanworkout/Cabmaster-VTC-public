from courses.forms import ReservationForm
from courses.models import Course
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Worker


@login_required(login_url="login")
def worker_profile(request, pk):
    """Worker profile view, here he can see his courses and submit some"""

    if request.method != "GET":
        # If method is not GET
        return JsonResponse({"error": "Bad Request"}, status=400)

    try:
        worker = request.user.worker

        # Ensure that the worker accessing the profile matches the logged-in user
        if worker.id != int(pk):
            # redirect to their own profile
            return redirect(reverse("worker_profile", args=[worker.id]))

        worker = get_object_or_404(Worker, id=pk)

        courses = Course.objects.filter(worker=pk, status="pending")

        add_course_form = ReservationForm()

        return render(
            request,
            "workers/worker_profile.html",
            {"courses": courses, "worker": worker, "add_course_form": add_course_form},
        )

    except ObjectDoesNotExist:
        # Handle the RelatedObjectDoesNotExist error
        return redirect("home")


@login_required(login_url="login")
def worker_profile_archives(request, pk):
    """Worker profile view, here he can see his archived courses"""

    try:
        worker = request.user.worker

        # Ensure that the worker accessing the profile matches the logged-in user
        if worker.id != int(pk):
            # redirect to their own profile
            return redirect(reverse("worker_profile", args=[worker.id]))

        worker = get_object_or_404(Worker, id=pk)

        archived_status = ["done", "cancelled"]
        courses = Course.objects.filter(worker=pk, status__in=archived_status)

        return render(
            request,
            "workers/worker_profile_archives.html",
            {"courses": courses, "worker": worker},
        )

    except ObjectDoesNotExist:
        # Handle the RelatedObjectDoesNotExist error
        return redirect("home")


def worker_contact(request):
    if request.method == "GET":
        return render(request, "workers/worker_contact.html")
    else:
        return JsonResponse({"error": "Bad Request"}, status=400)