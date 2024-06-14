from django.urls import path
from . import views
from . import api

urlpatterns = [
    path("rejoindre/", views.worker_contact, name="contact_worker"),
    path("profil/<int:pk>", views.worker_profile, name="worker_profile"),
    path("archives/<int:pk>", views.worker_profile_archives, name="worker_profile_archives"),
    ############################# API #############################
    path("api/update/", api.update_course, name="worker_update_course"),
    path("api/cancel/", api.cancel_course, name="worker_cancel_course"),
]