from django.contrib import admin
from django.urls import path, include

# For robots.txt
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home.urls")),
    path("partenaires/", include("workers.urls")),
    # path("clients/", include("customers.urls")),
    
    # ROBOT.TXT
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="home/robots.txt", content_type="text/plain"
        ),
    ),
]


handler404 = "home.views.error_404_view"