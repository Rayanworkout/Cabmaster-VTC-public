from django import forms

from .models import Course

from home.utils import get_time, get_date


class ReservationForm(forms.Form):
    """Custom form that mixes the customer and course model
    to make a reservation. here we CAN'T use form.save() because
    we have to create a customer and a course object at the same time"""

    customer_first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "booking-input-field mandatory prevent",
                "placeholder": "Prénom",
            }
        ),
    )
    customer_last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "booking-input-field mandatory prevent",
                "placeholder": "Nom",
            }
        ),
    )
    customer_email = forms.EmailField(
        max_length=254,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "booking-input-field prevent",
                "placeholder": "Email",
            }
        ),
    )
    customer_phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "booking-input-field prevent",
                "placeholder": "Tél",
            }
        ),
    )

    pickup_address = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "booking-input-field mandatory estimate-mandatory prevent",
                "placeholder": "Départ",
            }
        ),
    )
    destination = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "booking-input-field mandatory estimate-mandatory prevent",
                "placeholder": "Destination",
            }
        ),
    )

    happening_date = forms.CharField(
        initial=get_date(),
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "booking-input-field mandatory estimate-mandatory",
                "placeholder": "Date",
            }
        ),
    )

    happening_time = forms.CharField(
        initial=get_time(),
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "booking-input-field mandatory estimate-mandatory prevent",
                "placeholder": "Heure",
            }
        ),
    )

    course_type = forms.ChoiceField(
        choices=Course.TYPE_CHOICES,
        widget=forms.TextInput(
            attrs={"autofocus": True, "class": "booking-input-field"}
        ),
    )

    course_grade = forms.ChoiceField(
        choices=Course.GRADE_CHOICES,
        widget=forms.Select(
            attrs={
                "autofocus": True,
                "class": "mandatory estimate-mandatory booking-input-field text-dark",
            }
        ),
    )

    passengers = forms.ChoiceField(
        initial=0,
        choices=Course.PASSENGERS_CHOICES,
        widget=forms.Select(
            attrs={
                "autofocus": True,
                "class": "booking-input-field mandatory estimate-mandatory text-dark",
            }
        ),
    )

    payment_mode = forms.ChoiceField(
        choices=Course.PAYMENT_CHOICES,
        widget=forms.Select(
            attrs={"autofocus": True, "class": "booking-input-field text-dark"}
        ),
    )

    more_infos = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs={
                "autofocus": True,
                "class": "booking-input-field",
                "placeholder": "Informations Supplémentaires pour un service proche de vos attentes.",
                "style": "height: 100px;",
            }
        ),
    )
