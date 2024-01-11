from django.db import models

class Customer(models.Model):
    
    first_name = models.CharField("Prénom", max_length=50)
    
    last_name = models.CharField("Nom", max_length=50)
    
    email = models.EmailField("Email", max_length=254, unique=True)
    
    phone_number = models.CharField("Tél", max_length=12, unique=False, blank=True, null=True)
        
    def __str__(self):
        return self.last_name.capitalize()
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

