from courses.forms import ReservationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm, LoginForm


def home(request):
    """main home view"""
    form = ContactForm()
    return render(request, "home/index.html", {"form": form})


@ratelimit(key="user_or_ip", rate="5/m")
def login_user(request):
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"success": True}, safe=False)

            else:
                return JsonResponse({"success": False, "message": "wrong credentials"}, safe=False)

        else:
            return JsonResponse({"success": False, "message": "form not valid"}, safe=False)
    else:
        login_form = LoginForm()
        login_view = reverse("login")
        return render(
            request,
            "home/login.html",
            {
                "login_form": login_form,
                "login_view": login_view,
            },
        )


@login_required(login_url="home")
def logout_user(request):
    logout(request)
    return redirect("home")


def faq(request):
    return render(request, "home/faq.html")


def about(request):
    return render(request, "home/about_us.html")


def reservation(request):
    reservation_form = ReservationForm()

    # Getting reservation view url to check it inside the template
    reservation_view = reverse("reservation_page")

    return render(
        request,
        "home/reservation.html",
        {"reservation_form": reservation_form, "reservation_view": reservation_view},
    )


def legal_mentions(request):
    return render(request, "home/legal_mentions.html")


def error_404_view(request, exception):
    return render(request, "home/404.html", status=404)