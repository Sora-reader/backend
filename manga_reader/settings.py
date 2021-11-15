import copy
import logging
import os
from datetime import timedelta
from functools import partial
from pathlib import Path

import scrapy.utils.log
import sentry_sdk
from colorlog import ColoredFormatter
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger

###########
# Project #
###########

SHELL_PLUS_PRINT_SQL_TRUNCATE = None
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = "manga_reader.urls"
WSGI_APPLICATION = "manga_reader.wsgi.application"
WEBDRIVER_PATH = os.getenv("WEBDRIVER_PATH", None)

############
# Security #
############

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = int(os.getenv("DEBUG", 1))
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(" ")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

########
# Apps #
########

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "apps.api_docs",
    "apps.login.apps.LoginConfig",
    "apps.parse",
    "apps.core.apps.CoreConfig",
    "django_extensions",
    "django.contrib.postgres",
    "django_elasticsearch_dsl",
]

ELASTICSEARCH_DSL = {
    "default": {"hosts": os.getenv("ELASTICSEARCH_HOST", "localhost:92000")},
}

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
        "authtoken",
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

#######
# API #
#######

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (),
    "DEFAULT_AUTHENTICATION_CLASSES": (),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 20)),
}

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication."
    "default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

##############
# Middleware
##############

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

########
# CORS #
########

CORS_ALLOW_ALL_ORIGINS = True

############
# Database #
############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}

#################
# Authorization #
#################

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
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
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

STATIC_URL = "/static/"
STATIC_ROOT = "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REDIS_URL = os.getenv("REDIS_URL")

################
# Localization #
################

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


#############
# GlitchTip #
#############

SENTRY_DSN = os.getenv("SENTRY_DSN", "")
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
ignore_logger("django.security.DisallowedHost")

########
# Silk #
########

if DEBUG:
    INSTALLED_APPS.append("silk")
    MIDDLEWARE.append("silk.middleware.SilkyMiddleware")

##########
# Logging #
##########

COLORED_FORMAT = (
    "%(log_color)s%(levelname)-8s%(reset)s"
    "%(bold_white)s[%(asctime)s]%(reset)s "
    "%(log_color)s%(message)s%(reset)s"
)
COLORLESS_FORMAT = "%(levelname)-8s[%(asctime)s] %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"

SoraColoredLogger = partial(
    ColoredFormatter,
    datefmt=DATEFMT,
    log_colors={
        "DEBUG": "white",
        "INFO": "bold_cyan",
        "WARNING": "bold_yellow",
        "ERROR": "bold_red",
        "CRITICAL": "red,bg_white",
    },
)

color_formatter = SoraColoredLogger(COLORED_FORMAT)
colorless_formatter = logging.Formatter(COLORLESS_FORMAT, datefmt=DATEFMT)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "manga_reader.settings.SoraColoredLogger",
            "format": COLORED_FORMAT,
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "management": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

##########
# Scrapy #
##########

PROXY = os.getenv("PROXY")

_get_handler = copy.copy(scrapy.utils.log._get_handler)


def _get_handler_custom(*args, **kwargs):
    handler = _get_handler(*args, **kwargs)
    formatter = color_formatter
    if isinstance(handler, logging.FileHandler):
        formatter = colorless_formatter
    handler.setFormatter(formatter)
    return handler


scrapy.utils.log._get_handler = _get_handler_custom
