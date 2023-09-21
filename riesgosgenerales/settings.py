"""Django 4.2.1 settings for riesgosgenerales project."""

import os
import sys
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
    "django-insecure-hgcdf2#o+%k*6q(+=!$@3r$rok$4p=h9%azlf=g+8jh4rx*t_w"
)

ENV_DEBUG: str = os.environ.get("RRGG_DEBUG", "on")
ENV_DEBUG = ENV_DEBUG.lower()
if ENV_DEBUG in ("on", "true", "1"):
    DEBUG = True
elif ENV_DEBUG in ("off", "false", "0"):
    DEBUG = False
else:
    raise ValueError("Invalid ENV_DEBUG value")

ALLOWED_HOSTS: List[str] = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rrgg",
    "rrggweb",
    "rrggadmin",
]

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

ROOT_URLCONF = "riesgosgenerales.urls"

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
            "libraries": {"nomos": "nomos.template.defaulttags"},
        },
    },
]

WSGI_APPLICATION = "riesgosgenerales.wsgi.application"


# Database


DATABASES = {
    "default": (
        {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["LOCAL_DB_NAME"],
            "USER": os.environ["LOCAL_DB_USER"],
            "PASSWORD": os.environ["LOCAL_DB_PASSWORD"],
            "HOST": os.environ["LOCAL_DB_HOST"],
            "PORT": "5432",
        }
        if DEBUG
        else {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["RRGG_DB_NAME"],
            "USER": os.environ["RRGG_DB_USER"],
            "PASSWORD": os.environ["RRGG_DB_PASSWORD"],
            "HOST": os.environ["RRGG_DB_HOST"],
            "PORT": "5432",
        }
    )
}

# Logging

if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "rrgg-output": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "level": "DEBUG",
            },
        },
        "loggers": {
            "": {
                "handlers": ["rrgg-output"],
            },
        },
    }

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]


# Internationalization

LANGUAGE_CODE = "es"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_STORAGE = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )

# Media files (user uploaded files)

MEDIA_URL = "mediafiles/"
MEDIAFILES_DIRS = [BASE_DIR / "mediafiles"]
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

if not DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
    STATICFILES_STORAGE = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
