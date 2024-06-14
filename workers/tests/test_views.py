from courses.forms import ReservationForm
from courses.models import Course
from django.test import Client, TestCase
from django.urls import reverse
from home.models import CustomUser
from customers.models import Customer
from workers.models import Worker


class TestWorkersViewsAndAPI(TestCase):
    """Some tests are triggering rate limit
    so they cannot be runned all at once"""

    def setUp(self) -> None:
        self.client = Client()

        # Urls
        self.worker_profile_url = reverse("worker_profile", args=[1])
        self.worker_profile_archives_url = reverse("worker_profile_archives", args=[1])
        self.worker_contact_url = reverse("contact_worker")
        self.update_course_url = reverse("worker_update_course")
        self.cancel_course_url = reverse("worker_cancel_course")
        self.reservation_url = reverse("reserve_course")

        # Create a user with worker user_type
        self.user_worker = CustomUser.objects.create_user(
            email="test@email.fr",
            password="password",
            user_type="worker",
        )

        # Create a user with customer user_type
        self.user_customer = CustomUser.objects.create_user(
            email="customer@email.fr",
            password="password",
            user_type="customer",
        )

        # Create a customer
        self.customer = Customer.objects.create(
            first_name="customer_first_name",
            last_name="customer_last_name",
            email="customer@email.fr",
            phone_number="0601010101",
        )

        # Create a worker
        self.worker = Worker.objects.create(
            user=self.user_worker,
            phone_number="0600000000",
            telegram="test",
            company="test",
            secteur_activite="test",
        )

        # Create a course
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

    # # Worker Profile
    # def test_worker_profile_POST_not_authenticated(self):
    #     response = self.client.post(self.worker_profile_url)

    #     # Redirect to login page
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(
    #         response, f"{reverse('login')}?next={self.worker_profile_url}"
    #     )

    def test_worker_profile_POST_authenticated_as_worker(self):
        # Authenticate user
        self.client.force_login(self.user_worker)

        response = self.client.post(self.worker_profile_url)

        # Bad Request
        self.assertEquals(response.status_code, 400)

    def test_worker_profile_POST_authenticated_as_customer(self):
        # Authenticate user
        self.client.force_login(self.user_customer)

        response = self.client.post(self.worker_profile_url)

        # Bad Request
        self.assertEquals(response.status_code, 400)

    # def test_worker_profile_GET_not_authenticated(self):
    #     response = self.client.get(self.worker_profile_url)

    #     # Redirect to login page
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(
    #         response, f"{reverse('login')}?next={self.worker_profile_url}"
    #     )

    def test_worker_profile_GET_authenticated_as_worker_SUCCESS(self):
        # Authenticate Worker
        self.client.force_login(self.user_worker)

        response = self.client.get(self.worker_profile_url)

        # Success
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "workers/worker_profile.html")

        # Check form instance
        form = response.context["add_course_form"]
        self.assertIsInstance(form, ReservationForm)

        worker = response.context["worker"]
        self.assertEquals(worker, self.worker)

    def test_worker_profile_GET_authenticated_as_customer(self):
        # Authenticate Customer
        self.client.force_login(self.user_customer)

        response = self.client.get(self.worker_profile_url)

        # Redirect to home page
        self.assertEquals(response.status_code, 302)

    
    def test_worker_profile_redirect_wrong_worker(self):
        # Authenticate Worker
        self.client.force_login(self.user_worker)

        self.new_url = reverse("worker_profile", args=[2]) # Second worker

        response = self.client.get(self.new_url)

        # Redirect to their own profile
        self.assertEquals(response.status_code, 302)


    # Worker Profile Archives
    # def test_worker_profile_archives_GET_not_authenticated(self):
    #     response = self.client.get(self.worker_profile_archives_url)

    #     # Redirect to login page
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(
    #         response, f"{reverse('login')}?next={self.worker_profile_archives_url}"
    #     )

    # def test_worker_profile_archives_GET_authenticated_as_worker_SUCCESS(self):
    #     # Authenticate Worker
    #     self.client.force_login(self.user_worker)

    #     response = self.client.get(self.worker_profile_archives_url)

    #     # Success
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, "workers/worker_profile_archives.html")

    #     worker = response.context["worker"]
    #     self.assertEquals(worker, self.worker)

    # def test_worker_profile_archives_GET_authenticated_as_customer(self):
        # Authenticate Customer
        self.client.force_login(self.user_customer)

        response = self.client.get(self.worker_profile_archives_url)

        # Redirect to home page
        self.assertEquals(response.status_code, 302)

    def test_worker_profile_archives_GET_authenticated_as_wrong_worker(self):
        # Authenticate Customer
        self.client.force_login(self.user_worker)

        self.new_url = reverse("worker_profile_archives", args=[2])

        response = self.client.get(self.new_url)

        # redirect to their own profile
        self.assertEquals(response.status_code, 302)

    # Worker Contact
    def test_worker_contact_GET(self):
        response = self.client.get(self.worker_contact_url)

        # Success
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "workers/worker_contact.html")

    def test_worker_contact_POST_FAIL(self):
        
        response = self.client.post(self.worker_contact_url)

        # Bad Request
        self.assertEquals(response.status_code, 400)

    # API - Update Course
    def test_update_course_GET_authenticated(self):
        
        # Authenticate Worker
        self.client.force_login(self.user_worker)
        
        response = self.client.get(self.update_course_url)

        # Bad Request
        self.assertEquals(response.status_code, 400)
    
    # def test_update_course_POST(self):
    #     # Authenticate Worker
    #     self.client.force_login(self.user_worker)
        
    #     response = self.client.post(self.update_course_url)
        
    #     # Bad Request
    #     self.assertEquals(response.status_code, 400)
    
    # # def test_update_course_PUT_not_authenticated(self):
    #     response = self.client.put(self.update_course_url)

    #     # Redirect to login page
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(
    #         response, f"{reverse('login')}?next={self.update_course_url}"
    #     )

    def test_update_course_PUT_authenticated_SUCCESS(self):
        # Make the course from the worker
        self.course.worker = self.worker
        self.course.save()

        # Authenticate Worker
        self.client.force_login(self.user_worker)

        data = {
            "id": self.course.id,
            "customer_last_name": "test",
            "date": "12/12/2023",
            "time": "12:00",
            "pickup_address": "test",
            "destination": "test",
        }

        response = self.client.put(
            self.update_course_url, data=data, content_type="application/json"
        )

        # Success
        self.assertEquals(response.status_code, 204)

    def test_update_course_PUT_SUCCESS_is_well_updated(self):
        # Make the course from the worker
        self.course.worker = self.worker
        self.course.save()

        # Authenticate Worker
        self.client.force_login(self.user_worker)

        data = {
            "id": self.course.id,
            "customer_last_name": "test",
            "date": "12/12/2023",
            "time": "12:00",
            "pickup_address": "new_address",
            "destination": "new_destination",
        }

        self.client.put(
            self.update_course_url, data=data, content_type="application/json"
        )

        # Check if course has been well updated
        course = Course.objects.get(id=self.course.id)
        self.assertEquals(course.pickup_address, "new_address")
        self.assertEquals(course.destination, "new_destination")
    
    def test_update_course_PUT_SUCCESS_is_well_updated_customer(self):
        # Make the course from the worker
        self.course.worker = self.worker
        self.course.save()

        # Authenticate Worker
        self.client.force_login(self.user_worker)

        data = {
            "id": self.course.id,
            "customer_last_name": "new_last_name",
            "date": "12/12/2023",
            "time": "12:00",
            "pickup_address": "test",
            "destination": "test",
        }

        self.client.put(
            self.update_course_url, data=data, content_type="application/json"
        )

        # Check if customer has been well updated
        customer = Customer.objects.get(id=self.customer.id)
        self.assertEquals(customer.last_name, "new_last_name")
    
    def test_update_course_PUT_authenticated_as_wrong_worker(self):
        # Authenticate Worker
        self.client.force_login(self.user_worker)

        # Create a course

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

        # But this course is NOT from this worker
        data = {
            "id": self.course.id,
            "customer_last_name": "test",
            "date": "12/12/2023",
            "time": "12:00",
            "pickup_address": "test",
            "destination": "test",
        }

        response = self.client.put(
            self.update_course_url, data=data, content_type="application/json"
        )

        # Bad request
        self.assertEquals(response.status_code, 403)

    def test_update_course_PUT_authenticated_as_worker_course_does_not_exist(self):
        # Authenticate Worker
        self.client.force_login(self.user_worker)

        data = {
            "id": 1,
            "customer_last_name": "test",
            "date": "12/12/2023",
            "time": "12:00",
            "pickup_address": "test",
            "destination": "test",
        }

        response = self.client.put(self.update_course_url, data=data)

        # Success
        self.assertEquals(response.status_code, 400)

    def test_update_course_PUT_authenticated_as_customer(self):
        # Authenticate Customer
        self.client.force_login(self.user_customer)

        data = {
            "id": 1,
            "customer_last_name": "test",
            "date": "12/12/2023",
            "time": "12:00",
            "pickup_address": "test",
            "destination": "test",
        }

        response = self.client.put(self.update_course_url, data=data)

        # Bad Request
        self.assertEquals(response.status_code, 400)
    
    # API - Create Course
    def test_create_course_worker_authenticated(self):
        """Check if worker is taken into account when creating a course
        as well as its commission"""
        # Authenticate Worker
        self.client.force_login(self.user_worker)
        
        data = {
            "customer_email": "testeeeee@email.fr",
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
        }

        response = self.client.post(self.reservation_url, data=data)

        # Success
        self.assertEquals(response.status_code, 201)
        
        # Check if the course has been well created by THIS worker
        course = Course.objects.filter(customer__email=data["customer_email"]).first()
        
        self.assertEquals(course.worker, self.worker)
        worker_commission = course.course_price * 0.05
        self.assertEquals(course.worker_commission, worker_commission)
    
    # API - Cancel Course
    def test_cancel_course_GET_authenticated(self):
        
        # Authenticate Worker
        self.client.force_login(self.user_worker)
        
        response = self.client.get(self.cancel_course_url)

        # Bad Request
        self.assertEquals(response.status_code, 400)
    
    def test_cancel_course_POST(self):
        # Authenticate Worker
        self.client.force_login(self.user_worker)
        
        response = self.client.post(self.cancel_course_url)
        
        # Bad Request
        self.assertEquals(response.status_code, 400)
        
    def test_cancel_course_PUT_not_authenticated(self):
        response = self.client.put(self.cancel_course_url)

        # Redirect to login page
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login')}?next={self.cancel_course_url}"
        )

    def test_cancel_course_PUT_authenticated_without_reason(self):
        # Make the course from the worker
        self.course.worker = self.worker
        self.course.save()

        # Authenticate Worker
        self.client.force_login(self.user_worker)

        data = {
            "id": self.course.id,
        }

        response = self.client.put(
            self.cancel_course_url, data=data, content_type="application/json"
        )

        # Bad request, "please provide a reason"
        self.assertEquals(response.status_code, 400)
    
    def test_cancel_course_PUT_authenticated_SUCCESS(self):
        # Make the course from the worker
        self.course.worker = self.worker
        self.course.save()

        # Authenticate Worker
        self.client.force_login(self.user_worker)

        data = {
            "id": self.course.id,
            "reason": "test",
        }

        response = self.client.put(
            self.cancel_course_url, data=data, content_type="application/json"
        )

        # Success
        self.assertEquals(response.status_code, 204)

    def test_cancel_course_SUCCESS_is_well_cancelled(self):
        # Make the course from the worker
        self.course.worker = self.worker
        self.course.save()

        # Authenticate Worker
        self.client.force_login(self.user_worker)

        data = {
            "id": self.course.id,
            "reason": "test",
        }

        self.client.put(
            self.cancel_course_url, data=data, content_type="application/json"
        )

        # Check if course has been well cancelled
        course = Course.objects.get(id=self.course.id)
        self.assertEquals(course.status, "cancelled")
    
    def test_cancel_course_PUT_authenticated_as_wrong_worker(self):
        # Authenticate Worker
        self.client.force_login(self.user_worker)

        # Create a course

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

        # But this course is NOT from this worker
        data = {
            "id": self.course.id,
            "reason": "test",
        }

        response = self.client.put(
            self.cancel_course_url, data=data, content_type="application/json"
        )

        # Bad request
        self.assertEquals(response.status_code, 403)
        
    def test_cancel_course_PUT_authenticated_as_worker_course_does_not_exist(self):
        # Authenticate Worker
        self.client.force_login(self.user_worker)

        data = {
            # Course does not exist
            "id": 99,
            "reason": "test",
        }

        response = self.client.put(self.cancel_course_url, data=data)

        # Bad request
        self.assertEquals(response.status_code, 400)
        
    def test_cancel_course_PUT_authenticated_as_customer(self):
        # Authenticate Customer
        self.client.force_login(self.user_customer)

        data = {
            "id": 1,
            "reason": "test",
        }

        response = self.client.put(self.cancel_course_url, data=data)

        # Bad Request
        self.assertEquals(response.status_code, 400)