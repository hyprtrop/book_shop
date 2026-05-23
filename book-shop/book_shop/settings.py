"""
Django settings for book_shop project (Phase 1 + Phase 2 hardened).

Reads all secrets and environment-specific config from environment variables
so the same image can run locally, in dev, in test, and in prod with no rebuild.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


def _env_bool(name, default=False):
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


# --------------------------------------------------------------------- #
# Core
# --------------------------------------------------------------------- #
SECRET_KEY = _env("SECRET_KEY", required=True)

DEBUG = _env_bool("DEBUG", default=False)

ALLOWED_HOSTS = [
    h.strip()
    for h in _env("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in _env("CSRF_TRUSTED_ORIGINS", default="").split(",")
    if o.strip()
]


# --------------------------------------------------------------------- #
# Apps / middleware / urls
# --------------------------------------------------------------------- #
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "books",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # safety net if nginx isn't in front
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "book_shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "book_shop.wsgi.application"


# --------------------------------------------------------------------- #
# Database — PostgreSQL (replaces SQLite)
# --------------------------------------------------------------------- #
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME":     _env("POSTGRES_DB",       required=True),
        "USER":     _env("POSTGRES_USER",     required=True),
        "PASSWORD": _env("POSTGRES_PASSWORD", required=True),
        "HOST":     _env("POSTGRES_HOST",     default="db"),
        "PORT":     _env("POSTGRES_PORT",     default="5432"),
        "CONN_MAX_AGE": 60,
    }
}


# --------------------------------------------------------------------- #
# Passwords / i18n
# --------------------------------------------------------------------- #
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------- #
# Static files — collectstatic writes here; nginx serves from the volume
# --------------------------------------------------------------------- #
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
