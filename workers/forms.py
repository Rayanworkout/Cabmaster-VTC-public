from django import forms

from .models import Worker
from home.models import CustomUser


class WorkerRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Prénom"}),
    )

    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Nom"}),
    )

    email = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Adresse email"}),
    )

    company = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Entreprise Actuelle"}),
    )

    CHOICES = (
        ("hotel", "Hôtellerie"),
        ("restaurant", "Restauration"),
        ("autre", "Autre"),
    )

    secteur_activite = forms.CharField(
        max_length=50, widget=forms.Select(choices=CHOICES), label="Secteur d'Activité"
    )

    phone_number = forms.CharField(
        max_length=10,
        required=True,
        help_text="Entrer les numéros sans aucun séparateur.",
        widget=forms.TextInput(attrs={"placeholder": "Numéro de téléphone"}),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmer le mot de passe"}),
    )

    class Meta:
        model = Worker
        fields = [
            "first_name",
            "last_name",
            "email",
            "company",
            "secteur_activite",
            "phone_number",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        """Overriding form's save function in order to to save the user FIRST
        otherwise it can't be linked to the worker and causes OperationalError (UNIQUE constraint failed)
        """

        user = CustomUser.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            user_type="worker",
            is_active=False,
        )

        worker = Worker.objects.create(
            user=user,
            company=self.cleaned_data["company"],
            phone_number=self.cleaned_data["phone_number"],
            secteur_activite=self.cleaned_data["secteur_activite"],
        )

        if commit:
            user.save()
            worker.save()

        return user


