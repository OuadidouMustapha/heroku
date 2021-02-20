"""
Django settings for orchest project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from django.contrib.messages import constants as messages
import os
from decouple import config, Csv

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


# List of host/domain names that the project can serve
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Set the X-Frame-Options header to allow outgoing HttpResponse from the same origin
# NOTE : The following setting is needed to allow connection between Django apps and Dash
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common.apps.CommonConfig',
    'stock.apps.StockConfig',
    'forecasting.apps.ForecastingConfig',
    'deployment.apps.DeploymentConfig',
    'account.apps.AccountConfig',
    # See details: https://github.com/GibbsConsulting/django-plotly-dash
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'channels',
    'channels_redis',
    'mptt',  # See details: https://github.com/django-mptt/django-mptt
    'corsheaders',
    'import_export',
    'extra_views',
    'crispy_forms',
    'widget_tweaks',
    'django_filters',
    'django_tables2',
    'django_select2',
    'notifications',
    'rest_framework',
    # 'import_export_celery',
    'inventory.apps.InventoryConfig',
    'rest_framework',
    'purchase.apps.PurchaseConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Call Dash app directely instead of using it as an embedded frame
    'django_plotly_dash.middleware.BaseMiddleware',
]

ROOT_URLCONF = 'orchest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Access the MEDIA_URL in template
                # https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'orchest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
    }

}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'  # 'en-us' 'fr'
TIME_ZONE = 'Africa/Casablanca'
USE_I18N = True
USE_L10N = True
# USE_TZ = True

LOCALE_PATHS = (
    os.path.abspath(os.path.join(BASE_DIR, 'conf', 'locale')),
)


# Asynchronous routing configuration required for Dash (TODO for notification)
# Ref: https://medium.com/@ranjanmp/django-channels-2-notifications-def476d46c86
ASGI_APPLICATION = 'orchest.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379), ],
        }
    }
}

# Staticfiles finders for locating dash app assets and related files
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder'
]

# Message framework setting
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Plotly components containing static content that should
# be handled by the Django staticfiles infrastructure

PLOTLY_COMPONENTS = [
    # Common components
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    # django-plotly-dash components
    'dpd_components',
    # # static support if serving local assets
    # 'dpd_static_support',

    # # Other components, as needed
    'dash_bootstrap_components',
]

PLOTLY_DASH = {
    # Name of view wrapping function
    "view_decorator": "django_plotly_dash.access.login_required",
}
# TODO REST API AFTER
# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_RENDERER_CLASSES': (
#         'rest_framework.renderers.JSONRenderer',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#     'rest_framework.authentication.SessionAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
#     'PAGE_SIZE': 100,

#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# TODO config AWS S3 settings and add an environment variable
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATICFILES_LOCATION = 'static'

# Use custom user model
AUTH_USER_MODEL = 'account.CustomUser'

LOGIN_URL = '/account/login'
# Redirect page after login
LOGIN_REDIRECT_URL = "/stock"
# Redirect page after logout
LOGOUT_REDIRECT_URL = "/account/login"

# # SMTP Server TODO use MailGun or SendGrid
# # for development purposes Django lets us store emails as a file
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp/sent_emails')


# to test with SMTP use the following
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = 'abdeltif.b@gclgroup.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True


# raise th emax limit for file upload
# Default: 2621440 (i.e. 2.5 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440*7

###### DRAFT CELERY DJANGO##########
# django-import-export settings
# IMPORT_EXPORT_USE_TRANSACTIONS = True
# # Configure the location of celery module setup
# IMPORT_EXPORT_CELERY_INIT_MODULE = "orchest.celery"
# IMPORT_EXPORT_CELERY_MODELS = {
#     "Winner": {
#         'app_label': 'stock',
#         'model_name': 'Product',
#     }
# }

# # Celery Configuration Options
# CELERY_TIMEZONE = "Australia/Tasmania"
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60


# Crispy settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Use the built-in Bootstrap4 template for django-tables2
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

# DRF settings
REST_FRAMEWORK = {
    # TODO Use json version DRF in production mode
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),


    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

}

# JWT response handler
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'account.utils.my_jwt_response_handler'
}

# CORS setting
# CORS_ALLOWED_ORIGINS = [
#     'orchestanalytics.com',
#     'www.orchestanalytics.com',
#     'orchest-static.s3.amazonaws.com'
# ]

# FIXME Security warning! Allow CORS for trusted hosts only
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'localhost:3000/'
# )


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
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            # 'filename': '/path/to/django/debug.log',
            'filename': os.path.join(BASE_DIR, 'tmp/log', 'debug.log'),
            # 'maxBytes': 1024*1024*15, # 15MB
            # 'backupCount': 10,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
