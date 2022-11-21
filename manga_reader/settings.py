import copy
import logging
import logging.config
import os
from functools import partial
from pathlib import Path

import dj_database_url
import environ
import scrapy.utils.log
import sentry_sdk
from colorlog import ColoredFormatter
from django.core.management import BaseCommand
from sentry_sdk.integrations.django import DjangoIntegration

from apps.parse.types import CacheType
from apps.typesense_bind.client import create_client

# TODO: docstrings in utils and stuff

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(lambda a: a.split(" "), ["*"]),
    DJANGO_LOG_LEVEL=(str, "INFO"),
    REDIS_URL=(str, "redis://localhost:8883"),
    TYPESENSE_HOST=(str, "localhost"),
    TYPESENSE_PROTOCOL=(str, "http"),
    TYPESENSE_API_KEY=(str, "api"),
    PROXY=(str, ""),
    GOOGLE_CLIENT=(str, ""),
    GOOGLE_SECRET=(str, ""),
    APM_NAME=(str, "rq-worker"),
    SENTRY_DSN=(str, ""),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Django debug toolbar IPs
INTERNAL_IPS = ["127.0.0.1"]

###########
# Project #
###########

SHELL_PLUS_PRINT_SQL_TRUNCATE = None
ROOT_URLCONF = "manga_reader.urls"
WSGI_APPLICATION = "manga_reader.wsgi.application"

ELASTIC_APM = {
    "SERVICE_NAME": env("APM_NAME"),
    "SECRET_TOKEN": "",
    "SERVER_URL": "http://70.34.249.112:8200",
    "ENVIRONMENT": "production",
    "DJANGO_TRANSACTION_NAME_FROM_ROUTE": True,
}

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

############
# Security #
############

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Stub so it works while using cloudflare, I don't want to fix it for now, so here it is
CSRF_TRUSTED_ORIGINS = [
    "https://sora-reader.app",
    "https://*.sora-reader.app",
    "http://localhost:3000",
]

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "baggage",
    "sentry-trace",
]

SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_NAME = "sessionId"

############
# Scraping #
############

PROXY = env("PROXY")
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
}
REDIS_URL = env("REDIS_URL")
RQ_QUEUES = {
    "default": {
        "URL": REDIS_URL,
    }
}

TS_CLIENT = create_client(
    env("TYPESENSE_HOST"), env("TYPESENSE_API_KEY"), env("TYPESENSE_PROTOCOL")
)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    },
    CacheType.detail.value: {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{REDIS_URL}/2",
    },
    CacheType.chapter.value: {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{REDIS_URL}/3",
    },
    CacheType.image.value: {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{REDIS_URL}/4",
    },
}

########
# Apps #
########

INSTALLED_APPS = [
    "elasticapm.contrib.django",
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_extensions",
    "ninja_jwt",
    "ninja_extra",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_rq",
    "apps.typesense_bind.apps.TypesenseBindConfig",
    "apps.core",
    "apps.authentication.apps.AuthenticationConfig",
    "apps.manga.apps.MangaConfig",
    "apps.parse",
    "apps.readmanga.apps.Config",
    "apps.mangachan.apps.Config",
]
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

#########
# ADMIN #
#########

JAZZMIN_SETTINGS = {
    "site_title": "Admin",
    "site_header": "Sora",
    # logo for your site, must be present in static files, used for favicon and brand on top left
    "site_logo": "favicon.ico",
    "welcome_sign": "Admin panel",
    "copyright": '<a target="_blank" href="https://github.com/sora-reader">Sora</a>',
    "search_model": "parse.manga",
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {
            "name": "Support",
            "url": "https://github.com/sora-reader/backend/issues",
            "new_window": True,
        },
    ],
    #############
    # Side Menu #
    #############
    "show_sidebar": True,
    "navigation_expanded": True,
    "sidebar_fixed": True,
    "hide_apps": ["token_blacklist"],
    "hide_models": ["auth.group"],
    "icons": {
        "parse.manga": "fas fa-book-open",
        "parse.author": "fas fa-user-edit",
        "parse.genre": "fas fa-theater-masks",
        "parse.person": "fas fa-user-edit",
        "parse.chapter": "fas fa-file-alt",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",
        "core.taskcontrol": "fas fa-tasks",
    },
    "order_with_respect_to": [
        "parse",
        "parse.manga",
        "parse.author",
        "parse.genre",
        "auth",
        "login",
        "core",
    ],
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "admin/css/custom_jazzmin.css",
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}
JAZZMIN_UI_TWEAKS = {
    "sidebar_fixed": True,
    "actions_sticky_top": True,
}

##############
# Middleware
##############

MIDDLEWARE = [
    "elasticapm.contrib.django.middleware.TracingMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

############
# Database #
############

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
DATABASES = {
    "default": dj_database_url.config(default="postgres://postgres:postgres@localhost:8882/sora"),
}

#################
# Authorization #
#################

LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_VERIFICATION = "optional"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env("GOOGLE_CLIENT"),
            "secret": env("GOOGLE_SECRET"),
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

###########
# Serving #
###########

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

STATIC_URL = "static/"
STATIC_ROOT = "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

################
# Localization #
################

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

##########
# Logging #
##########

# Colored formatting into masses

COLORED_FORMAT = (
    "%(log_color)s%(levelname)-8s%(reset)s"
    "%(bold_white)s[%(asctime)s]%(reset)s "
    "%(log_color)s%(message)s%(reset)s"
)
COLORLESS_FORMAT = "%(levelname)-8s[%(asctime)s] %(message)s"
LOGGER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

SoraColoredLogger = partial(
    ColoredFormatter,
    datefmt=LOGGER_DATE_FORMAT,
    log_colors={
        "DEBUG": "white",
        "INFO": "bold_cyan",
        "WARNING": "bold_yellow",
        "ERROR": "bold_red",
        "CRITICAL": "red,bg_white",
    },
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "colored": {
            "()": SoraColoredLogger,
            "format": COLORED_FORMAT,
        }
    },
    "handlers": {
        "elasticapm": {
            "level": "INFO",
            "class": "elasticapm.contrib.django.handlers.LoggingHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "level": "INFO",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "elasticapm"],
            "level": "INFO",
            "propagate": True,
        },
        "system": {
            "handlers": ["console", "elasticapm"],
            "level": "INFO",
            "propagate": False,
        },
        "scrapyscript": {
            "handlers": ["console", "elasticapm"],
            "level": "INFO",
            "propagate": False,
        },
        # Log errors from the Elastic APM module to the console (recommended)
        "elasticapm.errors": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Hijack Scrapy's logging

_get_handler = copy.copy(scrapy.utils.log._get_handler)  # noqa


def _get_handler_custom(*args, **kwargs):
    handler = _get_handler(*args, **kwargs)
    formatter = SoraColoredLogger(COLORED_FORMAT)
    if isinstance(handler, logging.FileHandler):
        formatter = logging.Formatter(COLORLESS_FORMAT, datefmt=LOGGER_DATE_FORMAT)
    handler.setFormatter(formatter)
    return handler


scrapy.utils.log._get_handler = _get_handler_custom

# Hack into BaseCommand to use logging instead of stdout/stderr

_system_logger = logging.getLogger("system")


class _StdoutLoggingStub:
    def write(self, arg, *args, **kwargs):
        _system_logger.info(arg.strip("\n"))

    @staticmethod
    def flush(*args, **kwargs):
        pass


class _StderrLoggingStub:
    def write(self, arg, *args, **kwargs):
        _system_logger.error(arg.strip("\n"))

    @staticmethod
    def flush(*args, **kwargs):
        pass


_base_command_init = BaseCommand.__init__


def _init_patch_stdio(self, *args, **kwargs):
    _base_command_init(self, *args, **kwargs)
    self.stdout = _StdoutLoggingStub()
    self.stderr = _StderrLoggingStub()


BaseCommand.__init__ = _init_patch_stdio
