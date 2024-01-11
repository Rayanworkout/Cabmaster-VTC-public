from django.test import TestCase

from courses.models import Course
from customers.models import Customer
from home.models import CustomUser, Contact, Invoice, BondeReservation


class TestHomeCustomUserModel(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            email="user@email.com",
            password="userpassword",
        )
    
    def test_create_user(self):
        
        self.assertEqual(self.user.email, "user@email.com")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        
    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(
            email="superuser@email.com",
            password="superuserpassword",)
        
        self.assertEqual(user.email, "superuser@email.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_type_default_value(self):
        self.assertEqual(self.user.user_type, "customer")
      
    def test_user_str_method(self):
        self.assertEqual(self.user.__str__(), f"{self.user.first_name} {self.user.last_name}")
        
    def test_user_verbose_name(self):
        self.assertEqual(self.user._meta.verbose_name, "Utilisateur")
    
    def test_user_verbose_name_plural(self):
        self.assertEqual(self.user._meta.verbose_name_plural, "Utilisateurs")
    
class TestHomeContactModel(TestCase):
    def setUp(self) -> None:
        self.contact = Contact.objects.create(
            name="contact_name",
            email="contact_email",
            phone_number="0601010101",
            message="contact_message",
        )
    
    def test_contact_creation(self):
        self.assertEqual(self.contact.__str__(), f"{self.contact.subject}: {self.contact.message}")
        self.assertEqual(self.contact.name, "contact_name")
        self.assertEqual(self.contact.email, "contact_email")
        self.assertEqual(self.contact.phone_number, "0601010101")
        self.assertEqual(self.contact.message, "contact_message")
       
    def test_contact_verbose_name(self):
        self.assertEqual(self.contact._meta.verbose_name, "Contact")
    
    def test_contact_verbose_name_plural(self):
        self.assertEqual(self.contact._meta.verbose_name_plural, "Contacts")
        
    def test_contact_default_handled_value(self):
        self.assertEqual(self.contact.handled, False)
    

class TestHomeInvoiceModel(TestCase):
    
    def setUp(self) -> None:
        
        self.customer = Customer.objects.create(
            first_name="customer_first_name",
            last_name="customer_last_name",
            email="customer_email",
            phone_number="0601010101",
        )
        
        self.course = Course.objects.create(
            customer=self.customer,
            course_price=100,
            cabmaster_commission=10,
            worker_commission=0,
            worker=None,
            small_cases=0,
            big_cases=0,
            course_grade="standard",
            happening_datetime="2021-01-01 12:00",
            pickup_address="avenue de la viste, marseille",
            destination="gare saint charles, marseille",
            payment_mode="cash",
            passengers=1,
            comments="",
        )
        
        self.invoice = Invoice.objects.create(
            course = self.course,
            customer=self.customer,
            paid=False,
            ht_price=100,
            ttc_price=110,
            payment_method="cash",   
        )

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.__str__(), f"Facture {self.course.id} {self.customer}")
        self.assertEqual(self.invoice.course, self.course)
        self.assertEqual(self.invoice.customer, self.customer)
        self.assertEqual(self.invoice.paid, False)
        self.assertEqual(self.invoice.ht_price, 100)
        self.assertEqual(self.invoice.ttc_price, 110)
        self.assertEqual(self.invoice.payment_method, "cash")
        
    def test_invoice_verbose_name(self):
        self.assertEqual(self.invoice._meta.verbose_name, "Facture")
        
    def test_invoice_verbose_name_plural(self):
        self.assertEqual(self.invoice._meta.verbose_name_plural, "Factures")
    
    def test_invoice_str_method(self):
        self.assertEqual(self.invoice.__str__(), f"Facture {self.course.id} {self.customer}")
        
        
        
        
class TestHomeBondeReservationModel(TestCase):
    pass
