from django.test import TestCase
from django.urls import resolve, reverse

from workers.views import worker_contact
from workers.api import update_course


class TestWorkerUrls(TestCase):
    
    def test_contact_worker_url_is_resolved(self):
        url = reverse("contact_worker")
        self.assertEquals(resolve(url).func, worker_contact)
        
    
    def test_worker_profile_url_is_resolved(self):
        url = reverse("worker_profile", args=[1])
        resolver = resolve(url)
        self.assertEquals(resolver.view_name, "worker_profile")
        self.assertEquals(resolver.kwargs["pk"], 1)
    
    def test_worker_profile_archives_url_is_resolved(self):
        url = reverse("worker_profile_archives", args=[1])
        resolver = resolve(url)
        self.assertEquals(resolver.view_name, "worker_profile_archives")
        self.assertEquals(resolver.kwargs["pk"], 1)
    
    def test_worker_update_course_url_is_resolved(self):
        url = reverse("worker_update_course")
        self.assertEquals(resolve(url).func, update_course)