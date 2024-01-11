import json

from django.test import Client, TestCase
from django.urls import reverse

from home.models import CustomUser
from home.forms import ContactForm, LoginForm


class TestHomeViews(TestCase):
    """Class to test my views, I use client to simulate a user requests
    and then I test the response status code and the template used"""

    def setUp(self):
        """Method to set up the data for the tests"""
        # Client to make requests
        self.client = Client()

        # Urls
        self.home_url = reverse("home")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

        # Create a user
        self.user = CustomUser.objects.create_user(
            email="test@email.com",
            password="password",
            first_name="test",
            last_name="test",
            user_type="worker",
        )

    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        
        form = response.context['form']
        self.assertIsInstance(form, ContactForm)

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home/login.html")
        
        form = response.context['login_form']
        self.assertIsInstance(form, LoginForm)

    def test_login_POST_success(self):
        # csrf_token = self.client.get(self.login_url).cookies[
        #     "csrftoken"
        # ]

        data = {
            # "csrfmiddlewaretoken": csrf_token,  (OPTIONAL)
            "email": self.user.email,
            "password": "password", # password is hashed when saved so we can't use self.user.password
        }
        

        response = self.client.post(
            self.login_url,
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode("utf-8"))
        
        # Login success
        self.assertTrue(json_response['success'])
      
    def test_login_POST_failure(self):
        # csrf_token = self.client.get(self.login_url).cookies[
        #     "csrftoken"
        # ]

        data = {
            # "csrfmiddlewaretoken": csrf_token,  (OPTIONAL)
            "email": self.user.email,
            "password": "wrongpassword",
        }

        response = self.client.post(
            self.login_url,
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode("utf-8"))
        
        # Login failure
        self.assertFalse(json_response['success'])

    def test_login_POST_form_not_valid(self):
        # csrf_token = self.client.get(self.login_url).cookies[
        #     "csrftoken"
        # ]

        data = {
            # "csrfmiddlewaretoken": csrf_token,  (OPTIONAL)
            "email": self.user.email,
            "password": "",
        }

        response = self.client.post(
            self.login_url,
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode("utf-8"))
        
        # Form not valid
        self.assertFalse(json_response['success'])
        
        
    # RATE LIMIT OK
    # def test_login_rate_limit(self):
        
    #     # Try to login with no time between requests
    #     for i in range(6):
    #         response = self.client.get(self.login_url)
    #         if i > 1:
    #             self.assertEqual(response.status_code, 403)

    def test_logout_GET(self):
        # Log in the user
        self.client.login(username=self.user.email, password='password')
        
        # Make a GET request to the logout URL
        response = self.client.get(self.logout_url)
        
        # Check the response status code and redirection
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, self.home_url, status_code=302, target_status_code=200)
        
        # Check if the user is logged out
        user_logged_in = '_auth_user_id' in self.client.session
        self.assertFalse(user_logged_in, "User should be logged out after logout view")
    
    def test_faq_GET(self):
        response = self.client.get(reverse("faq"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home/faq.html")
        
    def test_about_GET(self):
        response = self.client.get(reverse("about"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home/about_us.html")
        
    def test_reservation_GET(self):
        response = self.client.get(reverse("reservation_page"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home/reservation.html")
    
    def test_404_page_GET(self):
        response = self.client.get('/not-existing-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "home/404.html")
        
        
    
    def test_legal_mentions_GET(self):
        response = self.client.get(reverse("legal_mentions"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home/legal_mentions.html")