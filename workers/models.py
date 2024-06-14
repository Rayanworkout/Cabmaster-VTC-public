from django.db import models

from home.models import CustomUser

class Worker(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    phone_number = models.CharField("Tél", max_length=10)
    
    telegram = models.CharField("Telegram", max_length=50, null=True, blank=True)
            
    company = models.CharField("Entreprise", max_length=50)
    
    secteur_activite = models.CharField("Secteur", max_length=50, null=True, blank=True)
    
    
    def __str__(self):
        return self.user.first_name.capitalize() + " " + self.user.last_name.capitalize()
    
    class Meta: 
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        

