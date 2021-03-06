"""
Django settings for pandas_grader project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "iamy!^p_7q_9v)c&u1v)nt0284-vzyp9(6+v%(gkkhofv_7j5!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #lol

ALLOWED_HOSTS = ["*"]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Gotta be able to delete all the tings
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240 

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
    "constance",
    "constance.backends.database",
]

MIDDLEWARE = [
    # "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pandas_grader.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "pandas_grader.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# DB settings for postgres.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        'NAME': 'ds100_autograder_db',
        'USER': 'ds100',
        'PASSWORD': 'safetyoff',
        'HOST': 'localhost',
        'PORT': '',
    }
}

"""
# DB Settings for postgres
# Used instructions from:
# https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DS100_AUTOGRADER_DB',
        'USER': 'ds100',
        'PASSWORD': 'safetyoff',
        'HOST': 'localhost',
        'PORT': '',
    }
}
"""



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = "/static/"


# Django-Constance Configuration
# https://django-constance.readthedocs.io/en/latest/
CONSTANCE_CONFIG = {
    "DOCKER_IMAGE": ("wwhuang/jhub-gofer:latest", "The grading environment"),
    "PARALLELISM": (200, "How many jobs to run in parallel"),
    "NAMESPACE": ("data100-staging", "The JupyterHub K8s namespace to run job"),
    "ADDRESS": ("http://grading.ds100.org:8080", "Current server address"),
}
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
