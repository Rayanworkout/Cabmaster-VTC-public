from django.test import TestCase
from home.models import CustomUser
from drivers.models import Driver



# class Driver(models.Model):
#     """Driver model that is linked to the custom user model
#     in a one-to-one relationship"""

#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

#     company = models.CharField("Entreprise", max_length=50)

#     siret = models.CharField("SIRET", max_length=14, null=True, blank=True)

#     phone_number = models.CharField("Tél", max_length=10)

#     telegram = models.CharField("Télégram", max_length=50, null=True, blank=True)

#     address = models.CharField("Adresse", max_length=100)

#     city = models.CharField("Ville", max_length=50)

#     zip_code = models.CharField("CP", max_length=10)

#     country = models.CharField("Pays", max_length=50, default="France")

#     def __str__(self):
#         return f"{self.user.first_name.capitalize()} {self.user.last_name.capitalize()}"

#     class Meta:
#         verbose_name = "Chauffeur"
#         verbose_name_plural = "Chauffeurs"



class TestDriversModels(TestCase):
    
    def setUp(self) -> None:
        # Create a user
        self.user = CustomUser.objects.create_user(
            email="test@user.fr",
            password="testpassword",
            user_type="driver",
            first_name="test",
            last_name="test",
            )
        
        # Create a driver
        self.driver = Driver.objects.create(
            user=self.user,
            company="testcompany",
            siret="12345678901234",
            phone_number="0123456789",
            telegram="testtelegram",
            address="testaddress",
            city="testcity",
            zip_code="12345",
            country="testcountry",)
    
    
    def test_driver_str(self):
        self.assertEqual(str(self.driver), "Test Test")
        
    def test_driver_verbose_name(self):
        self.assertEqual(str(Driver._meta.verbose_name), "Chauffeur")
    
    def test_driver_verbose_name_plural(self):
        self.assertEqual(str(Driver._meta.verbose_name_plural), "Chauffeurs")
        
    def test_driver_user(self):
        self.assertEqual(self.driver.user, self.user)
        
    def test_driver_company(self):
        self.assertEqual(self.driver.company, "testcompany")
        
    def test_driver_siret(self):
        self.assertEqual(self.driver.siret, "12345678901234")
        
        
    def test_driver_phone_number(self):
        self.assertEqual(self.driver.phone_number, "0123456789")
        
    def test_driver_telegram(self):
        self.assertEqual(self.driver.telegram, "testtelegram")
        
    def test_driver_address(self):
        self.assertEqual(self.driver.address, "testaddress")
        
    def test_driver_city(self):
        self.assertEqual(self.driver.city, "testcity")
        
    def test_driver_zip_code(self):
        self.assertEqual(self.driver.zip_code, "12345")
        
    def test_driver_country(self):
        self.assertEqual(self.driver.country, "testcountry")        
        