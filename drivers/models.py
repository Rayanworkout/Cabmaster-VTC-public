from django.db import models

from home.models import CustomUser


class Driver(models.Model):
    """Driver model that is linked to the custom user model
    in a one-to-one relationship"""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    company = models.CharField("Entreprise", max_length=50)

    siret = models.CharField("SIRET", max_length=14, null=True, blank=True)

    phone_number = models.CharField("Tél", max_length=12)

    telegram = models.CharField("Télégram", max_length=50, null=True, blank=True)

    address = models.CharField("Adresse", max_length=100)

    city = models.CharField("Ville", max_length=50)

    zip_code = models.CharField("CP", max_length=10)

    country = models.CharField("Pays", max_length=50, default="France")

    def __str__(self):
        return f"{self.user.first_name.capitalize()} {self.user.last_name.capitalize()}"

    class Meta:
        verbose_name = "Chauffeur"
        verbose_name_plural = "Chauffeurs"
