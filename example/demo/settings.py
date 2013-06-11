#-*- coding: utf-8 -*-

import os

PRJ_PATH = os.path.abspath(os.path.curdir)

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    ("Alice Bloggs", "alice@example.com"),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   "django.db.backends.sqlite3",
        'NAME':     "inline_media_demo.db",
        'USER':     "", 
        'PASSWORD': "", 
        'HOST':     "", 
        'PORT':     "",
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Brussels"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PRJ_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PRJ_PATH, "server-static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PRJ_PATH, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = "v2824l&2-n+4zznbsk9c-ap5i)b3e8b+%*a=dxqlahm^%)68jn"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = "urls"

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    'django.contrib.messages',
    "django.contrib.staticfiles",
    "django.contrib.admin",

    "sorl.thumbnail",
    "tagging",
    "inline_media",

    "demo.articles",
    # "south",
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple' 
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'inline_media': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

import logging
from sorl.thumbnail.log import ThumbnailLogHandler

handler = ThumbnailLogHandler()
handler.setLevel(logging.ERROR)
logging.getLogger("sorl.thumbnail").addHandler(handler)

THUMBNAIL_BACKEND = "inline_media.sorl_backends.AutoFormatBackend"
THUMBNAIL_FORMAT = "JPEG"

# ADMIN_IMAGES_PATH = "%s/admin/img/admin" % STATIC_URL # Django 1.3

INLINE_MEDIA_TEXTAREA_ATTRS = {
    'default': { # default widget attributes, can be overriden on
                 # a per app_label.model basis
        'style': 'font: 12px monospace'
    },
    'articles.article': { # widget attributes for app_label.model
        'body': { 'rows': 20 } # field 'body'
    }
}

INLINE_MEDIA_CUSTOM_SIZES = {
    'inline_media.picture':    { 'large': 310 },
    'inline_media.pictureset': { 
        'small': None,
        'large': (288, 240),
    }
}
