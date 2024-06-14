from django.test import SimpleTestCase
from django.urls import resolve, reverse
from home.api import (
    contact,
    download_br,
    download_invoice,
    estimate_price,
    reserve_course,
)
from home.views import (
    about,
    faq,
    home,
    legal_mentions,
    login_user,
    logout_user,
    reservation,
)


class TestHomeUrls(SimpleTestCase):
    def test_about_url_is_resolved(self):
        url = reverse("about")
        self.assertEquals(resolve(url).func, about)

    def test_list_url_is_resolved(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func, home)
    
    def test_faq_url_is_resolved(self):
        url = reverse("faq")
        self.assertEquals(resolve(url).func, faq)
        
    def test_legal_mentions_url_is_resolved(self):
        url = reverse("legal_mentions")
        self.assertEquals(resolve(url).func, legal_mentions)
        
    def test_login_register_url_is_resolved(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func, login_user)
        
    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func, logout_user)
        
    def test_reservation_url_is_resolved(self):
        url = reverse("reservation_page")
        self.assertEquals(resolve(url).func, reservation)




class TestApiUrls(SimpleTestCase):
    def test_contact_url_is_resolved(self):
        url = reverse("contact")
        self.assertEquals(resolve(url).func, contact)

    def test_download_br_url_is_resolved(self):
        url = reverse("download_br", args=[1])
        resolver = resolve(url)
        
        self.assertEqual(url, '/br/api/create/1')
        
        self.assertEquals(resolver.func, download_br)
        
        self.assertEqual(resolver.kwargs['pk'], 1)
    
    def test_download_invoice_url_is_resolved(self):
        url = reverse("download_invoice", args=[1])
        resolver = resolve(url)
        
        self.assertEqual(url, '/api/invoice/create/1')
        
        self.assertEquals(resolver.func, download_invoice)
        self.assertEqual(resolver.kwargs['pk'], 1)

    
    def test_estimate_price_url_is_resolved(self):
        url = reverse("estimate_price", args=["origin", "destination", "course_grade"])
        resolver = resolve(url)
        
        self.assertEqual(url, '/api/estimate/origin/destination/course_grade')
        
        self.assertEquals(resolver.func, estimate_price)
        
        # Check if resolved URL captures the arguments correctly
        self.assertEqual(resolver.kwargs['origin'], 'origin')
        self.assertEqual(resolver.kwargs['destination'], 'destination')
        self.assertEqual(resolver.kwargs['course_grade'], 'course_grade')


    def test_reserve_course_url_is_resolved(self):
        url = reverse("reserve_course")
        self.assertEquals(resolve(url).func, reserve_course)
