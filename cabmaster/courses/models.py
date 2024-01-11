from django.db import models

from customers.models import Customer
from drivers.models import Driver
from workers.models import Worker


class Course(models.Model):
    """Each course is related to a customer, a driver and a worker.
    We CANNOT delete a customer, a driver or a worker if they are related to a course.
    This way we preserve data integrity."""

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, null=True, blank=True
    )

    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, null=True, blank=True)

    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, null=True, blank=True)

    pickup_address = models.CharField("Départ", max_length=200)

    destination = models.CharField("Destination", max_length=200)

    duration = models.IntegerField("Durée", null=True, blank=True)

    course_price = models.IntegerField("Prix", null=True)

    worker_commission = models.FloatField(
        "Commission Partenaire", null=True, blank=True, default=0
    )

    cabmaster_commission = models.FloatField(
        "Commission Cabmaster", null=True, blank=True, default=0
    )

    created_at = models.DateTimeField("Création", auto_now_add=True)

    happening_datetime = models.DateTimeField("Date")

    STATUS_CHOICES = (
        ("pending", "En Attente"),
        ("done", "Validée"),
        ("cancelled", "Annulée"),
    )

    status = models.CharField(
        "Statut", max_length=50, default="pending", choices=STATUS_CHOICES
    )

    TYPE_CHOICES = (
        ("classic", "Trajet"),
        ("disposition", "Mise à Disposition"),
    )
    course_type = models.CharField(
        "Type", max_length=50, default="classic", choices=TYPE_CHOICES
    )

    GRADE_CHOICES = (
        ("", "Catégorie"),
        ("standard", "Éco Confort"),
        ("berline", "Premium"),
        ("van", "Van"),
    )

    course_grade = models.CharField(
        "Grade", max_length=50, default="standard", choices=GRADE_CHOICES
    )

    PAYMENT_CHOICES = (
        ("", "Mode de Paiement"),
        ("cash", "Espèces"),
        ("card", "Carte Bancaire"),
        ("online", "En Ligne"),
    )
    payment_mode = models.CharField(
        "Paiement", max_length=10, default="cash", choices=PAYMENT_CHOICES
    )

    PASSENGERS_CHOICES = [[i, str(i)] for i in range(1, 9)]
    PASSENGERS_CHOICES.insert(0, ["", "Passagers"])

    passengers = models.IntegerField("Passagers", default=1)

    small_cases = models.IntegerField("Petites Valises", default=0)
    big_cases = models.IntegerField("Grandes Valises", default=0)

    comments = models.TextField("Commentaires", max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.customer} / {self.driver}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
