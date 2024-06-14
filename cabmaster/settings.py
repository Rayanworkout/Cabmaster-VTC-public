from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


############### PROD SETTINGS #####################

DEBUG = False

ALLOWED_HOSTS = ["www.cabmaster.fr", "cabmaster.fr", "127.0.0.1"]


INSTALLED_APPS = [
    ############################
    # MY APPS
    ############################
    "home.apps.HomeConfig",
    "courses.apps.CoursesConfig",
    "workers.apps.WorkersConfig",
    "customers.apps.CustomersConfig",
    "drivers.apps.DriversConfig",
    "whitenoise",
    ############################
    # THIRD PARTY APPS
    ############################
    ############################
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# USING CUSTOM AUTH USER MODEL TO ALLOW USERS TO LOGIN WITH EMAIL
# THIS CUSTOM USER MODEL EXTENDS THE ABSTRACT USER MODEL
AUTH_USER_MODEL = "home.CustomUser"

# ADDING THE CUSTOM BACKEND TO THE AUTHENTICATION BACKENDS
AUTHENTICATION_BACKENDS = [
    "home.backends.EmailBackend",
]

# SETTING THE COOKIE EXPIRATION TIME TO 12 HOURS
SESSION_COOKIE_AGE = 60 * 60 * 12  # 12 hours

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cabmaster.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cabmaster.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db", "cabmaster.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static_files")
STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SETTINGS FOR EMAIL BACKEND

EMAIL_SENDER_NAME = "Équipe Cabmaster"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

SECRET_KEY = "SECRET_KEY"

EMAIL_HOST_USER = "contact.cabmaster@gmail.com"
EMAIL_HOST_PASSWORD = "PASSWORD"

EMAIL_USE_TLS = True
