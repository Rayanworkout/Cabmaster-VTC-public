from customers.models import Customer
from django.db.utils import IntegrityError
from django.test import TestCase


class TestCustomerModel(TestCase):
    
    def setUp(self) -> None:
        # Create a customer
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="test@email.fr",
            phone_number="0123456789",
        )
    
    def test_customer_creation(self):
        self.assertTrue(isinstance(self.customer, Customer))
        self.assertEquals(self.customer.__str__(), "Doe")
        
    def test_customer_first_name_label(self):
        field_label = self.customer._meta.get_field("first_name").verbose_name
        self.assertEquals(field_label, "Prénom")
    
    def test_customer_last_name_label(self):
        field_label = self.customer._meta.get_field("last_name").verbose_name
        self.assertEquals(field_label, "Nom")
    
    def test_customer_email_label(self):
        field_label = self.customer._meta.get_field("email").verbose_name
        self.assertEquals(field_label, "Email")
        
    def test_customer_phone_number_label(self):
        field_label = self.customer._meta.get_field("phone_number").verbose_name
        self.assertEquals(field_label, "Tél")
        
    def test_customer_first_name_max_length(self):
        max_length = self.customer._meta.get_field("first_name").max_length
        self.assertEquals(max_length, 50)
        
    def test_customer_last_name_max_length(self):
        max_length = self.customer._meta.get_field("last_name").max_length
        self.assertEquals(max_length, 50)
        
    def test_customer_email_max_length(self):
        max_length = self.customer._meta.get_field("email").max_length
        self.assertEquals(max_length, 254)
        
    def test_customer_phone_number_max_length(self):
        max_length = self.customer._meta.get_field("phone_number").max_length
        self.assertEquals(max_length, 50)
    
    def test_customer_object_name_is_last_name_capitalize(self):
        expected_object_name = self.customer.last_name.capitalize()
        self.assertEquals(expected_object_name, str(self.customer))
        
    def test_customer_verbose_name_plural(self):
        self.assertEquals(str(Customer._meta.verbose_name_plural), "Clients")
        
    def test_customer_verbose_name(self):
        self.assertEquals(str(Customer._meta.verbose_name), "Client")

    def test_unique_email(self):
        # Ensure that email uniqueness is working
        with self.assertRaises(IntegrityError):
            # Trying to create another customer with the same email should raise IntegrityError
            Customer.objects.create(
                first_name="Jane",
                last_name="Smith",
                email="test@email.fr",  # Reusing the same email
                phone_number="9876543210",
            )

    
        
