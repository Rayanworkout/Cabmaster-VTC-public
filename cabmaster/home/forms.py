from django import forms
from django.contrib.auth import get_user_model

from .models import Contact

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=50,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Email", "type": "email", "class": "booking-input-field"}
        ),
    )

    password = forms.CharField(
        required=True,
        max_length=50,
        label="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mot de passe", "class": "booking-input-field", "type": "password"}
        ),
    )


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Nom*", "type": "text", "class": "booking-input-field contact-field"}),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email*", "type": "email", "class": "booking-input-field contact-field"}),
    )

    phone_number = forms.CharField(
        required=False,
        max_length=12,
        widget=forms.TextInput(attrs={"placeholder": "Numéro de téléphone", "type": "tel", "class": "booking-input-field contact-field"}),
    )

    subject = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Objet*", "type": "text", "class": "booking-input-field contact-field"}),
    )

    message = forms.CharField(
        required=True,
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Comment pouvons-nous vous aider ?", "class": "booking-input-field contact-field", "style": "height:200px"
            }
        ),
    )

    class Meta:
        model = Contact
        fields = [
            "name",
            "phone_number",
            "email",
            "phone_number",
            "subject",
            "message",
        ]

