from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

########################################################################################
# CUSTOM USER MODEL
########################################################################################

class UserManager(BaseUserManager):
    """A custom manager to deal with emails as unique identifiers for auth
    and nut using username field"""
    
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """User model that uses email as the username field to login"""
    
    username = None
    email = models.EmailField(unique=True)
    
    USER_TYPE_CHOICES = (
        ("customer", "Client"),
        ("driver", "Chauffeur"),
        ("worker", "Partenaire"),
    )
    
    user_type = models.CharField("Catégorie", max_length=50, choices=USER_TYPE_CHOICES, default="customer")
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    



########################################################################################
# CONTACT FORM
########################################################################################

class Contact(models.Model):
    name = models.CharField("Nom", max_length=50)
    
    email = models.EmailField("Email")
    phone_number = models.CharField("Tél", max_length=50)

    subject = models.CharField("Objet", max_length=50)

    message = models.TextField("Message")

    created_at = models.DateTimeField("Création", auto_now_add=True)

    handled = models.BooleanField("Traité", default=False)
    
    
    def __str__(self) -> str:
        return f"{self.subject}: {self.message}"
    
    
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"



########################################################################################
# INVOICE and DRIVER DOCUMENT
########################################################################################


class Invoice(models.Model):
    # The invoice has the same ID as the course
    course = models.OneToOneField(
        "courses.Course", primary_key=True, on_delete=models.CASCADE,
    )

    # Each invoice is linked to a customer
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE,)

    paid = models.BooleanField("Réglée", default=False)

    ht_price = models.IntegerField("Prix HT")
    ttc_price = models.IntegerField("Prix TTC")

    PAYMENT_METHODS = (
        ("CB", "Carte bancaire"),
        ("ES", "Espèces"),
        ("VI", "Virement"),
    )
    payment_method = models.CharField("Paiement",
        max_length=50, choices=PAYMENT_METHODS,
    )

    created_at = models.DateTimeField("Création", auto_now_add=True)
    
    def __str__(self):
        return f"Facture {self.course.id} {self.customer}"
    
    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"



class BondeReservation(models.Model):
    course = models.OneToOneField(
        "courses.Course", primary_key=True, on_delete=models.CASCADE
    )

    created_at = models.DateTimeField("Création", auto_now_add=True)
    
    class Meta:
        verbose_name = "Bon de réservation"
        verbose_name_plural = "Bons de réservation"
    
