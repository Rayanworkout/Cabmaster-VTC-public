from courses.models import Course
from customers.models import Customer
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from drivers.models import Driver
from workers.models import Worker

from .models import Contact, CustomUser

admin.site.unregister(Group)

class InlineDriver(admin.StackedInline):
    model = Driver

class InlineWorker(admin.StackedInline):
    model = Worker


@admin.register(CustomUser)
class UserAdminConfig(UserAdmin):
    """A class to customize the admin panel for the CustomUser model.
    Things like the fields to display, the ordering, and the search fields"""

    # Adding Customer form with user form
    
    inlines = [InlineDriver, InlineWorker]

    ordering = ("-date_joined",)

    search_fields = ("email", "first_name", "last_name")

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "user_type",
        "date_joined",
    )

    list_editable = ("is_active",)
    list_filter = ("is_active", "user_type", "date_joined")

    # Arrangement des fields à la consultation / modification d'un User
    fieldsets = (
        (
            "Informations",
            {
                "fields": (
                    "user_type",
                    "email",
                    "first_name",
                    "last_name",
                    "date_joined",
                )
            },
        ),
        ("Statut", {"fields": ("is_active",)}),
    )

    # Arrangement des fields à la création d'un User
    add_fieldsets = (
        (
            "Informations",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "user_type",
                    "password1",
                    "password2",
                )
            },
        ),
        ("Statut", {"fields": ("is_active",)}),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """A class to customize the admin panel for the Customer model.
    Things like the fields to display, the ordering, and the search fields"""



    list_display = (
        "id",
        "last_name",
        "first_name",
        "phone_number",
        "email",
    )

    list_display_links = (
        "last_name",
        "first_name",
    )

    search_fields = ("id", "phone_number")



@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """A class to customize the admin panel for the Driver model.
    Things like the fields to display, the ordering, and the search fields"""

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        # Add a click to send email
        return obj.user.email

    def date_joined(self, obj):
        return obj.user.date_joined

    def is_active(self, obj):
        state = obj.user.is_active
        if state:
            return "✅"
        else:
            return "❌"

    def last_login(self, obj):
        return obj.user.last_login

    # Creating links for some entries
    def id_(self, obj):
        url = reverse("admin:home_customuser_change", args=(obj.user.id,))
        return format_html(
            f'<a href="{url}" style="font-weight: bold; border: 1px solid #21386a; padding: 5px; border-radius: 20px;">{obj.user.id}</a>'
        )

    def courses(self, obj):
        count = obj.course_set.count()
        if count > 0:
            url = (
                reverse("admin:courses_course_changelist")
                + "?"
                + urlencode({"driver__id": f"{obj.id}"})
            )
            return format_html(
                f'<a href="{url}" style="font-weight: bold; border: 1px solid #21386a; padding: 5px; border-radius: 20px;">{count}</a>'
            )
        else:
            return "-"

    last_name.short_description = "Nom"
    first_name.short_description = "Prénom"

    date_joined.short_description = "Date d'inscription"
    is_active.short_description = "Actif"

    last_login.short_description = "Dernière Connexion"

    id_.short_description = "ID"

    list_display = (
        "last_name",
        "first_name",
        "id_",
        "company",
        "siret",
        "phone_number",
        "email",
        "telegram",
        "courses",
        "is_active",
        "date_joined",
        "last_login",
    )

    list_display_links = (
        "last_name",
        "first_name",
    )

    search_fields = (
        "phone_number",
        "company",
        "siret",
        "telegram",
    )

    list_filter = ("company", )


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    """A class to customize the admin panel for the Worker model.
    Things like the fields to display, the ordering, and the search fields"""

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def date_joined(self, obj):
        return obj.user.date_joined

    def is_active(self, obj):
        state = obj.user.is_active
        if state:
            return "✅"
        else:
            return "❌"

    def last_login(self, obj):
        return obj.user.last_login

    # Creating links for some entries
    def id_(self, obj):
        url = reverse("admin:home_customuser_change", args=(obj.user.id,))
        return format_html(
            f'<a href="{url}" style="font-weight: bold; border: 1px solid #21386a; padding: 5px; border-radius: 20px;">{obj.user.id}</a>'
        )

    def courses(self, obj):
        count = obj.course_set.count()
        if count > 0:
            url = (
                reverse("admin:courses_course_changelist")
                + "?"
                + urlencode({"worker__id": f"{obj.id}"})
            )
            return format_html(
                f'<a href="{url}" style="font-weight: bold; border: 1px solid #21386a; padding: 5px; border-radius: 20px;">{count}</a>'
            )
        else:
            return "-"

    last_name.short_description = "Nom"
    first_name.short_description = "Prénom"

    date_joined.short_description = "Date d'inscription"
    is_active.short_description = "Actif"

    last_login.short_description = "Dernière Connexion"

    id_.short_description = "ID"

    list_display = (
        "last_name",
        "first_name",
        "id_",
        "company",
        "secteur_activite",
        "phone_number",
        "email",
        "telegram",
        "courses",
        "is_active",
        "date_joined",
        "last_login",
    )

    list_display_links = (
        "last_name",
        "first_name",
    )

    search_fields = ("company", "secteur_activite", "phone_number", "telegram")

    list_filter = ("company", "secteur_activite")



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """A class to customize the admin panel for the Course model.
    Things like the fields to display, the ordering, and the search fields"""
    
    
    def invoice_download(self, obj):
        url = f"/api/invoice/create/{obj.id}"

        return format_html(
                f'<a href="{url}" style="color: #46b0ce;">📥</a>'
            )
    
    def br_download(self, obj):
        url = f"/br/api/create/{obj.id}"

        return format_html(
                f'<a href="{url}" style="color: #46b0ce;">📥</a>'
            )

    
    def our_commission(self, obj):
        if obj.cabmaster_commission:
                return f"{int(round(obj.cabmaster_commission))} €"
            
    
    def prix_course(self, obj):
        return f"{int(round(obj.course_price))} €"
    
    def worker_commission_(self, obj):
        if obj.worker_commission:
            return f"{int(round(obj.worker_commission))} €"
        elif obj.worker_commission < 1:
            return "❌"
 

    def customer_name(self, obj):
        if obj.customer:
            customer = obj.customer
            url = reverse("admin:customers_customer_change", args=(customer.id,))

            return format_html(
                f'<a href="{url}" style="color: #46b0ce;">{customer.first_name} {customer.last_name}</a>'
            )

    def customer_phone(self, obj):
        if obj.customer:
            customer = obj.customer
            return customer.phone_number



    invoice_download.short_description = "Facture"
    br_download.short_description = "B.R."
    customer_name.short_description = "Client"
    customer_phone.short_description = "Tél"
    our_commission.short_description = "Commission Cabmaster"
    prix_course.short_description = "Prix"
    worker_commission_.short_description = "Commission Partenaire"

    ################################################

    def driver_name(self, obj):
        if obj.driver:
            driver = obj.driver

            url = reverse("admin:drivers_driver_change", args=(driver.id,))

            return format_html(
                f'<a href="{url}" style="color: #46b0ce;">{driver.user.first_name} {driver.user.last_name}</a>'
            )

    def driver_company(self, obj):
        if obj.driver:
            driver = obj.driver
            return driver.company

    def driver_phone(self, obj):
        if obj.driver:
            driver = obj.driver
            return driver.phone_number

    driver_name.short_description = "Chauffeur"
    driver_company.short_description = "Entreprise"
    driver_phone.short_description = "Tél"

    ################################################

    def worker_name(self, obj):
        if obj.worker:
            worker = obj.worker

            url = reverse("admin:workers_worker_change", args=(worker.id,))

            return format_html(
                f'<a href="{url}" style="color: #46b0ce;">{worker.user.first_name} {worker.user.last_name}</a>'
            )

    def worker_company(self, obj):
        if obj.worker:
            return obj.worker.company

    worker_name.short_description = "Partenaire"
    worker_company.short_description = "Entreprise"

    list_display = (
        "id",
        "pickup_address",
        "destination",
        "duration",
        "prix_course",
        "our_commission",
        "happening_datetime",
        "course_type",
        "course_grade",
        "status",
        #############################
        "customer_name",
        "customer_phone",
        #############################
        "driver_name",
        "driver_company",
        "driver_phone",
        #############################
        "worker_name",
        "worker_company",
        "worker_commission_",
        #############################
        "invoice_download",
        "br_download",
    )

    search_fields = (
        "status",
        "happening_datetime",
        "course_type",
        "course_grade",
        "course_price",
        "pickup_address",
        "destination",
    )

    list_filter = (
        "status",
        "course_grade",
        "course_type",
        "happening_datetime",
    )

    list_editable = ("status", "course_grade")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """A class to customize the admin panel for the Contact model.
    Things like the fields to display, the ordering, and the search fields"""


    list_display = (
        "id",
        "name",
        "email",
        "phone_number",
        "subject",
        "message",
        "created_at",
        "handled",
    )

    search_fields = (
        "name",
        "email",
        "phone_number",
        "subject",
        "message",
    )

    list_filter = ("handled",)

    list_editable = ("handled",)


