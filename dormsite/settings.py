# Django settings for dormsite project.
import djcelery
import dj_database_url
import os

import django.conf.global_settings as DEFAULT_SETTINGS

djcelery.setup_loader()


def bool_env(val):
    """Replaces string based environment values with Python booleans"""
    return True if os.environ.get(val, False) == 'True' else False


DEBUG = bool_env('DEBUG')
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Hiram', 'ibb41-4dormsite@hmvp.nl'),
)

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))


MANAGERS = ADMINS


DATABASES = {
    'default': dj_database_url.config(default='sqlite:///%s/database.sqlite3' % PROJECT_DIR)
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': '',                      # Or path to database file if using sqlite3.
#        'USER': '',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nl-NL'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_DIR + '/staticfiles'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'https://googledrive.com/host/0B5K79dR3ug0uRDRXV1lDb1FBVkU/' if not DEBUG else '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    "iplogin.context_processors.iplogin",
    'django.core.context_processors.request',
    'core.context_processors.site'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'iplogin.middleware.IPLoginMiddleware',
    'dormsite.middleware.LoginRequiredMiddleware',
    'dormsite.middleware.WhodidMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dormsite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dormsite.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'djcelery',
    'django_tables2',
    'kombu.transport.django',
    'core',
    'schedule',
    'residents',
    'balance',
    'iplogin',
    'south',
    'storages',
    'crispy_forms',
    'django.contrib.markup',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
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
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST')]

BROKER_BACKEND = 'django'

AUTH_USER_MODEL = 'residents.User'

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/user/login/'
IP_AUTH_USER = 'ibby'
IP_AUTH_IP = [os.environ.get('IPLOGIN_IP'), '127.0.0.1']

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'iplogin.backend.IPAuthBackend',
)

MONTH_DAY_FORMAT = "j F"

MONTHLY_FEE = 12.50

RESIDENTS_GROUP_NAME = 'Huisgenoten'
ELDER_GROUP_NAME = 'Huisoudste'

LOGIN_EXEMPT_URLS = [r'^static/', r'^user/password', r'^schedule/ical', r'^schedule/cron']

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = '%s/emails' % PROJECT_DIR

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_PASSWORD')
EMAIL_ERROR_ADDRESS = os.environ.get('DEFAULT_FROM_EMAIL')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_SUBJECT_PREFIX = '[Dormsite] '

STATICFILES_STORAGE = 'storages.backends.google_drive.GoogleDriveStorage' if not DEBUG else DEFAULT_SETTINGS.STATICFILES_STORAGE
GDRIVE_CLIENTSECRETS_LOCATION = PROJECT_DIR + '/client_secrets.json'
GDRIVE_CREDENTIALS_FILE = PROJECT_DIR + '/client_credentials.json'
GDRIVE_ROOT_FOLDER_NAME = 'staticfiles'


CRISPY_TEMPLATE_PACK = 'bootstrap'
CRISPY_FAIL_SILENTLY = not DEBUG
