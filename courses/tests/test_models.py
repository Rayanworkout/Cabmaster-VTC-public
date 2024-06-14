from courses.models import Course
from customers.models import Customer
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from drivers.models import Driver
from home.models import CustomUser
from workers.models import Worker


class TestCourse(TestCase):
    def setUp(self) -> None:
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

        # Create a user with worker user_type
        self.user_worker = CustomUser.objects.create_user(
            email="test@email.fr",
            password="password",
            user_type="worker",
        )

        # And a worker
        self.worker = Worker.objects.create(
            user=self.user_worker,
            phone_number="0600000000",
            telegram="test",
            company="test",
            secteur_activite="test",
        )
        
        # Create a user with driver user_type
        self.user_driver = CustomUser.objects.create_user(
            email="test@user.fr",
            password="testpassword",
            user_type="driver",
            first_name="test",
            last_name="test",
            )
        
        # Create a driver
        self.driver = Driver.objects.create(
            user=self.user_driver,
            company="testcompany",
            siret="12345678901234",
            phone_number="0123456789",
            telegram="testtelegram",
            address="testaddress",
            city="testcity",
            zip_code="12345",
            country="testcountry",)
    

    def test_course_creation(self):
        self.assertEqual(
            self.course.__str__(), f"{self.course.id} {self.customer_instance} / None"
        )
        self.assertEqual(self.course.customer, self.customer_instance)
        self.assertEqual(self.course.course_price, 100)
        self.assertEqual(self.course.cabmaster_commission, 10)
        self.assertEqual(self.course.worker_commission, 0)
        self.assertEqual(self.course.worker, None)
        self.assertEqual(self.course.small_cases, 0)
        self.assertEqual(self.course.big_cases, 0)
        self.assertEqual(self.course.course_grade, "standard")
        self.assertEqual(self.course.happening_datetime, "2021-01-01 12:00")
        self.assertEqual(self.course.pickup_address, "avenue de la viste, marseille")
        self.assertEqual(self.course.destination, "gare saint charles, marseille")
        self.assertEqual(self.course.payment_mode, "cash")
        self.assertEqual(self.course.passengers, 1)
        self.assertEqual(self.course.comments, "")

    def test_course_str_method(self):
        self.assertEqual(
            self.course.__str__(), f"{self.course.id} {self.customer_instance} / None"
        )

    def test_course_verbose_name(self):
        self.assertEqual(self.course._meta.verbose_name, "Course")

    def test_course_verbose_name_plural(self):
        self.assertEqual(self.course._meta.verbose_name_plural, "Courses")

    def test_course_status_default_value(self):
        self.assertEqual(self.course.status, "pending")

    def test_course_status_choices(self):
        self.assertEqual(
            self.course.STATUS_CHOICES,
            (
                ("pending", "En Attente"),
                ("done", "Validée"),
                ("cancelled", "Annulée"),
            ),
        )

    def test_course_type_default_value(self):
        self.assertEqual(self.course.course_type, "classic")

    def test_course_type_choices(self):
        self.assertEqual(
            self.course.TYPE_CHOICES,
            (
                ("classic", "Trajet"),
                ("disposition", "Mise à Disposition"),
            ),
        )

    def test_course_grade_default_value(self):
        self.assertEqual(self.course.course_grade, "standard")

    def test_course_grade_choices(self):
        self.assertEqual(
            self.course.GRADE_CHOICES,
            (
                ("", "Catégorie"),
                ("standard", "Éco Confort"),
                ("berline", "Premium"),
                ("van", "Van"),
            ),
        )

    def test_course_payment_mode_default_value(self):
        self.assertEqual(self.course.payment_mode, "cash")

    def test_course_payment_mode_choices(self):
        self.assertEqual(
            self.course.PAYMENT_CHOICES,
            (
                ("", "Mode de Paiement"),
                ("cash", "Espèces"),
                ("card", "Carte Bancaire"),
                ("online", "En Ligne"),
            ),
        )

    def test_course_passengers_choices(self):
        choices = [[i, str(i)] for i in range(1, 9)]
        choices.insert(0, ["", "Passagers"])
        self.assertEqual(self.course.PASSENGERS_CHOICES, choices)

    def test_course_comments_max_length(self):
        self.assertEqual(self.course._meta.get_field("comments").max_length, 1000)

    def test_course_comments_null(self):
        self.assertEqual(self.course._meta.get_field("comments").null, True)

    def test_course_comments_blank(self):
        self.assertEqual(self.course._meta.get_field("comments").blank, True)

    def test_course_happening_datetime_null(self):
        self.assertEqual(self.course._meta.get_field("happening_datetime").null, False)

    def test_course_happening_datetime_blank(self):
        self.assertEqual(self.course._meta.get_field("happening_datetime").blank, False)

    def test_course_happening_datetime_auto_now_add(self):
        self.assertEqual(
            self.course._meta.get_field("happening_datetime").auto_now_add, False
        )

    def test_customer_deletion_protect(self):
        with self.assertRaises(ProtectedError):
            self.customer_instance.delete()

    def test_driver_deletion_protect(self):
        # Make the driver drive the course
        self.course.driver = self.driver
        self.course.save()
        
        with self.assertRaises(ProtectedError):
            self.course.driver.delete()

    def test_worker_deletion_protect(self):
        # First assign a worker to the course
        self.course.worker = self.worker
        self.course.save()

        with self.assertRaises(ProtectedError):
            self.worker.delete()
