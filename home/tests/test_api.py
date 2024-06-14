from courses.models import Course
from customers.models import Customer
from django.test import Client, TestCase
from django.urls import reverse
from home.models import CustomUser


class TestHomeApi(TestCase):
    """Class to test reservation API, I use client to simulate a user requests
    and then I test the response status code"""

    def setUp(self):
        """Method to set up the data for the tests"""
        # Client to make requests
        self.client = Client()

        # Urls
        self.reserve_url = reverse("reserve_course")
        self.estimate_url = reverse(
            "estimate_price", args=["marseille", "paris", "standard"]
        )
        self.contact_url = reverse("contact")

        self.download_br_url = reverse("download_br", args=[99])

        self.login_url = reverse("login")

        self.download_invoice_url = reverse("download_invoice", args=[99])

        # Create a superuser
        self.superuser = CustomUser.objects.create_superuser(
            email="superuser@email.com",
            password="password",
            first_name="test",
            last_name="test",
        )

        # Create a user
        self.user = CustomUser.objects.create_user(
            email="normaluser@email.com",
            password="password",
            first_name="test",
            last_name="test",
        )

        # Create a customer and a course
        self.customer_instance = Customer.objects.create(
            first_name="customer_first_name",
            last_name="customer_last_name",
            email="customer@email.fr",
            phone_number="0601010101",
        )

        self.course = Course.objects.create(
            customer=self.customer_instance,
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

    def tearDown(self):
        """Method to delete the data after the tests"""
        Course.objects.all().delete()
        Customer.objects.all().delete()
        CustomUser.objects.all().delete()

    # RESERVATION ENDPOINT

    def test_reservation_GET(self):
        """Test the reservation endpoint with GET method"""

        response = self.client.get(self.reserve_url)

        self.assertEqual(response.status_code, 400)

    def test_reservation_POST_success(self):
        """Test the reservation endpoint"""

        data = {
            "customer_email": "mokranerayan@outlook.fr",
            "customer_first_name": "test",
            "customer_last_name": "test",
            "customer_phone_number": "0668506456",
            "pickup_address": "avenue de la viste, marseille",
            "destination": "gare saint charles, marseille",
            "passengers": 1,
            "course_grade": "standard",
            "payment_mode": "cash",
            "happening_date": "01/12/2023",
            "happening_time": "12:00",
            "small_cases": 0,
            "big_cases": 0,
            "comments": "test data",
        }

        response = self.client.post(self.reserve_url, data=data)
        self.assertEqual(response.status_code, 201)
        
        

    def test_reservation_SUCCESS_with_existing_customer(self):
        """Test the reservation endpoint with an existing customer"""

        # New course for the same customer
        self.course2 = Course.objects.create(
            customer=self.customer_instance,
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

        self.assertEqual(self.course2.customer, self.customer_instance)
        self.assertEqual(self.course2.customer.email, self.customer_instance.email)

    def test_reservation_POST_with_invalid_passengers_number(self):
        """Test the reservation endpoint with invalid passengers number
        to see if we get 400 status + ValidationError"""

        data = {
            "customer_email": "test@email.fr",
            "customer_first_name": "test",
            "customer_last_name": "test",
            "customer_phone_number": "0668506456",
            "pickup_address": "avenue de la viste, marseille",
            "destination": "gare saint charles, marseille",
            "passengers": "bad_value",  # Invalid passengers number
            "course_grade": "standard",
            "payment_mode": "cash",
            "happening_date": "01/12/2023",
            "happening_time": "12:00",
            "small_cases": 0,
            "big_cases": 0,
        }

        response = self.client.post(self.reserve_url, data=data)
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["error"], "ValidationError")

    # def test_reservation_POST_with_invalid_email(self):
    #     """Test the reservation endpoint with invalid email
    #     to see if we get 400 status + ValidationError"""

    #     data = {
    #         "customer_email": "bad_email",
    #         "customer_first_name": "test",
    #         "customer_last_name": "test",
    #         "customer_phone_number": "0668506456",
    #         "pickup_address": "avenue de la viste, marseille",
    #         "destination": "gare saint charles, marseille",
    #         "passengers": 1,
    #         "course_grade": "standard",
    #         "payment_mode": "cash",
    #         "happening_date": "01/12/2023",
    #         "happening_time": "12:00",
    #         "small_cases": 0,
    #         "big_cases": 0,
    #     }

    #     response = self.client.post(self.reserve_url, data=data)
    #     json_response = response.json()

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(json_response["error"], "ValidationError")

    # Rate limit prevent post tests to work at the same time

    def test_reservation_POST_with_invalid_phone(self):
        """Test the reservation endpoint with invalid phone number
        to see if we get 400 status + ValidationError"""

        data = {
            "customer_email": "good_email@test.com",
            "customer_first_name": "test",
            "customer_last_name": "test",
            "customer_phone_number": "0668504",
            "pickup_address": "avenue de la viste, marseille",
            "destination": "gare saint charles, marseille",
            "passengers": 1,
            "course_grade": "standard",
            "payment_mode": "cash",
            "happening_date": "01/12/2023",
            "happening_time": "12:00",
            "small_cases": 0,
            "big_cases": 0,
        }

        response = self.client.post(self.reserve_url, data=data)
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["error"], "ValidationError")

    def test_reservation_POST_with_bad_json_data(self):
        incomplete_data = {
            "_email": "mokranerayan@outlook.fr",
            "customer_fname": "test",
            "customer_lme": "test",
        }

        response = self.client.post(self.reserve_url, data=incomplete_data)

        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["error"], "TypeError")

    # def test_reservation_has_comments(self):
    #     """Test if the course has comments"""

    #     data = {
    #         "customer_email": "test@email.coom",
    #         "customer_first_name": "test",
    #         "customer_last_name": "test",
    #         "customer_phone_number": "0668506456",
    #         "pickup_address": "avenue de la viste, marseille",
    #         "destination": "gare saint charles, marseille",
    #         "passengers": 1,
    #         "course_grade": "standard",
    #         "payment_mode": "cash",
    #         "happening_date": "01/12/2023",
    #         "happening_time": "12:00",
    #         "small_cases": 0,
    #         "big_cases": 0,
    #         "comments": "test data",
    #     }

    #     # Create a course with comments
    #     response = self.client.post(self.reserve_url, data=data)
        
    #     self.assertEqual(response.status_code, 201)
        
    #     # Check if the course has comments
    #     course = Course.objects.get(id=2)
    #     self.assertEqual(course.comments, data["comments"])

    # def test_reservation_course_and_customer_exists(self):
    #     """Test if the course and the customer are well created"""

    #     data = {
    #         "customer_email": "mokranerayan@outlook.fr",
    #         "customer_first_name": "test",
    #         "customer_last_name": "test",
    #         "customer_phone_number": "+33668506456",
    #         "pickup_address": "avenue de la viste, marseille",
    #         "destination": "gare saint charles, marseille",
    #         "passengers": 1,
    #         "course_grade": "standard",
    #         "payment_mode": "cash",
    #         "happening_date": "01/12/2023",
    #         "happening_time": "12:00",
    #         "small_cases": 0,
    #         "big_cases": 0,
    #     }

    #     response = self.client.post(self.reserve_url, data=data)

    #     self.assertEqual(response.status_code, 201)

    #     customer_exists = Customer.objects.filter(email=data["customer_email"]).exists()

    #     self.assertTrue(customer_exists)

    #     customer = Customer.objects.get(email=data["customer_email"])

    #     self.assertEqual(customer.email, data["customer_email"])
    #     self.assertEqual(customer.first_name, data["customer_first_name"])
    #     self.assertEqual(customer.last_name, data["customer_last_name"])
    #     self.assertEqual(customer.phone_number, data["customer_phone_number"])

    ##############################################################################################

    # ESTIMATE ENDPOINT
    def test_estimate_POST(self):
        """Test the estimate endpoint with POST method"""

        response = self.client.post(self.estimate_url)

        self.assertEqual(response.status_code, 400)

    def test_estimate_GET_success(self):
        response = self.client.get(self.estimate_url)
        self.assertEqual(response.status_code, 200)

    def test_estimate_GET_with_invalid_address(self):
        # Invalid address
        self.estimate_url = reverse(
            "estimate_price", args=["bad_origin", "paris", "standard"]
        )

        response = self.client.get(self.estimate_url)

        self.assertEqual(response.status_code, 400)

    def test_estimate_GET_with_invalid_grade(self):
        # Invalid address
        self.estimate_url = reverse(
            "estimate_price", args=["marseille", "paris", "bad_grade"]
        )

        response = self.client.get(self.estimate_url)

        self.assertEqual(response.status_code, 400)

    # RATE LIMIT OK
    # def test_estimate_GET_rate_limit(self):
    #     """Test the rate limit of the estimate endpoint"""

    #     for i in range(6):
    #         response = self.client.get(self.estimate_url)
    #         if i > 5:
    #             self.assertEqual(response.status_code, 429)

    ##############################################################################################

    # CONTACT ENDPOINT
    def test_contact_GET(self):
        """Test the contact endpoint with GET method"""

        response = self.client.get(self.contact_url)

        self.assertEqual(response.status_code, 400)

    def test_contact_POST_success(self):
        data = {
            "name": "test",
            "email": "test@email.fr",
            "phone_number": "0668506456",
            "subject": "test",
            "message": "test",
        }

        response = self.client.post(self.contact_url, data=data)

        self.assertEqual(response.status_code, 201)

    def test_contact_POST_with_invalid_email(self):
        data = {
            "name": "test",
            "email": "bad_email",
            "phone_number": "0668506456",
            "subject": "test",
            "message": "test",
        }

        response = self.client.post(self.contact_url, data=data)

        self.assertEqual(response.status_code, 400)

    ################################################################################################

    # DOWNLOAD BR ENDPOINT
    def test_download_br_POST(self):
        """Test the download br endpoint with POST method"""

        # authenticate user
        self.client.force_login(self.superuser)

        response = self.client.post(self.download_br_url)

        self.assertEqual(response.status_code, 400)

    def test_download_br_no_authentication(self):
        response = self.client.get(self.download_br_url)

        # REDIRECT TO LOGIN PAGE
        self.assertEqual(response.status_code, 302)

    def test_download_br_with_authentication_NORMAL_USER(self):
        # Login success
        self.client.force_login(self.user)

        # Get the endpoint with authentication
        download_br_response = self.client.get(self.download_br_url)

        # FORBIDDEN
        self.assertEqual(download_br_response.status_code, 403)

    def test_download_br_with_authentication_SUPERUSER_course_does_not_exist(self):
        # Login suepruser
        self.client.force_login(self.superuser)

        # Get the endpoint with authentication as superuser
        download_br_response = self.client.get(self.download_br_url)

        # Course does not exist
        self.assertEqual(download_br_response.status_code, 400)

    def test_download_br_with_authentication_SUPERUSER_course_exists(self):
        # Login as superuser
        self.client.force_login(self.superuser)

        # Get the endpoint with authentication as superuser
        self.download_br_url = reverse("download_br", args=[self.course.id])

        download_br_response = self.client.get(self.download_br_url)

        # Course does not exist
        self.assertEqual(download_br_response.status_code, 200)

    ################################################################################################

    # DOWNLOAD INVOICE ENDPOINT

    def test_download_invoice_POST(self):
        """Test the download invoice endpoint with POST method"""

        # authenticate user
        self.client.force_login(self.superuser)
        response = self.client.post(self.download_invoice_url)

        self.assertEqual(response.status_code, 400)

    def test_download_invoice_no_authentication(self):
        response = self.client.get(self.download_invoice_url)

        # REDIRECT TO LOGIN PAGE
        self.assertEqual(response.status_code, 302)

    def test_download_invoice_with_authentication_NORMAL_USER(self):
        # Login as normal user
        self.client.force_login(self.user)

        # Get the endpoint with authentication
        download_invoice_response = self.client.get(self.download_invoice_url)

        # FORBIDDEN
        self.assertEqual(download_invoice_response.status_code, 403)

    def test_download_invoice_with_authentication_SUPERUSER_course_does_not_exist(self):
        # Login as superuser
        self.client.force_login(self.superuser)

        # Get the endpoint with authentication as superuser

        download_invoice_response = self.client.get(self.download_invoice_url)

        # Course does not exist
        self.assertEqual(download_invoice_response.status_code, 400)

    def test_download_invoice_with_authentication_SUPERUSER_course_exists_but_not_done(
        self,
    ):
        # Login as superuser
        self.client.force_login(self.superuser)

        # Get the endpoint with authentication as superuser
        self.download_invoice_url = reverse("download_invoice", args=[self.course.id])

        download_invoice_response = self.client.get(self.download_invoice_url)

        # Course exists but status != done
        self.assertEqual(download_invoice_response.status_code, 400)

    def test_download_invoice_with_authentication_SUPERUSER_course_exists_and_done(
        self,
    ):
        # Login as superuser
        self.client.force_login(self.superuser)

        # Change the status of the course to done
        self.course.status = "done"
        self.course.save()

        # Get the endpoint with authentication as superuser
        self.download_invoice_url = reverse("download_invoice", args=[self.course.id])

        download_invoice_response = self.client.get(self.download_invoice_url)

        # Course exists and status == done
        self.assertEqual(download_invoice_response.status_code, 200)
