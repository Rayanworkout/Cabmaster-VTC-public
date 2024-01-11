from django.urls import path
from . import views
from . import api


urlpatterns = [
    path("", views.home, name="home"),
    path("connexion/", views.login_user, name="login"),
    path("deconnexion/", views.logout_user, name="logout"),
    path("faq/", views.faq, name="faq"),
    path("about/", views.about, name="about"),
    path("reservation/", views.reservation, name="reservation_page"),
    path("mentions-legales/", views.legal_mentions, name="legal_mentions"),
    ############################# API #############################
    path("api/estimate/<str:origin>/<str:destination>/<str:course_grade>", api.estimate_price, name="estimate_price"),
    path("api/contact/", api.contact, name="contact"),
    path("api/reservation/create/", api.reserve_course, name="reserve_course"),
    path("api/invoice/create/<int:pk>", api.download_invoice, name="download_invoice"),
    path("br/api/create/<int:pk>", api.download_br, name="download_br"),
]
