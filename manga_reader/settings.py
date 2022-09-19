import os
from pathlib import Path

import dj_database_url
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(lambda a: a.split(" "), ["*"]),
    DJANGO_LOG_LEVEL=(str, "INFO"),
    REDIS_URL=(str, "redis://localhost:8883"),
    ELASTICSEARCH_HOST=(str, "localhost:9200"),
    PROXY=(str, ""),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

###########
# Project #
###########

SHELL_PLUS_PRINT_SQL_TRUNCATE = None
ROOT_URLCONF = "manga_reader.urls"
WSGI_APPLICATION = "manga_reader.wsgi.application"

############
# Security #
############

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CORS_ALLOW_ALL_ORIGINS = True

############
# Scraping #
############

PROXY = env("PROXY")
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
}
REDIS_URL = env("REDIS_URL")
ELASTICSEARCH_DSL = {
    "default": {"hosts": env("ELASTICSEARCH_HOST")},
}
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

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
    "corsheaders",
    "django_extensions",
    "django_elasticsearch_dsl",
    "apps.core.apps.CoreConfig",
    "apps.manga",
    "apps.parse",
]

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
USE_L10N = True
USE_TZ = True

##########
# Logging #
##########

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env("DJANGO_LOG_LEVEL"),
            "propagate": False,
        },
    },
}
