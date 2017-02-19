import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_inline_media_test',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.abspath(os.path.curdir), 'tests')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''


SECRET_KEY = 'v2824l&2-n+4zznbsk9c-ap5i)b3e8b+%*a=dxqlahm^%)68jn'


INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'sorl.thumbnail',
    'taggit',
    'inline_media',

    'inline_media.tests',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

ROOT_URLCONF = 'inline_media.tests.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
            ],
        },
    },
]


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'server-static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/media/"


THUMBNAIL_BACKEND = "inline_media.sorl_backends.AutoFormatBackend"
THUMBNAIL_FORMAT = "JPEG"

# THUMBNAIL_STORAGE = "inline_media.tests.storage.TestStorage"
# ADMIN_IMAGES_PATH = "%s/admin/img/admin" % STATIC_URL # Django 1.3

INLINE_MEDIA_TYPES = [
    'inline_media.picture',
    'inline_media.pictureset',
    'inline_media.tests.testmediamodel',
]

INLINE_MEDIA_CUSTOM_SIZES = {
    'inline_media.picture': {'mini': 81},
    'inline_media.pictureset': {
        # by default -> 'mini': None # see inline_media/conf/defaults.py
        'small': None
    }
}

INLINE_MEDIA_TEXTAREA_ATTRS = {
    'default': {
        'style': 'font: 13px monospace'
    },
    'tests.ModelTest': {
        'second_text': {'rows': '20'}
    }
}

INLINE_MEDIA_DEBUG = True
