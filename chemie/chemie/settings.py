"""
Django settings for chemie project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

if os.environ.get("DEBUG") == "False":
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'd)%%e$l#xa7xtvro#(%n)q)h$_399wth0i1^@hxrruqz$0&@zx'
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    ALLOWED_HOSTS = ['*']

ADMINS = [('Carl Johan Hambro', 'carljohan.hambro@gmail.com')]

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'chemie',
    'elections',
    'home',
    'news',
    'shitbox',
    'committees',
    'events',
    'lockers',
    'yearbook',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'customprofile',
    'sorl.thumbnail',
    'material',
    'mail_templated',
    "post_office",
    'wiki',
    'django.contrib.humanize',
    'django_nyt',
    'sekizai',
    'wiki.plugins.attachments',
    'wiki.plugins.images',
    'wiki.plugins.macros',
    'mptt',
    'haystack',
    'widget_tweaks',
    'rest_framework',
    'smart_selects',
    'ckeditor',
    'django.contrib.flatpages',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chemie.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
            ],
            'loaders': ['django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader']
        },
    }
]

if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [('django.template.loaders.cached.Loader',
                                           ['django.template.loaders.filesystem.Loader',
                                            'django.template.loaders.app_directories.Loader'])]

WSGI_APPLICATION = 'chemie.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db1.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'database',
            'PORT': '5432',
            'CONN_MAX_AGE': 600,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'hashers_passlib.phpass',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'nb'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "chemie/static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or ''
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or ''

NOCAPTCHA = True

EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST') or ''
EMAIL_PORT = os.environ.get('EMAIL_PORT') or 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') or ''
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') or ''
DEFAULT_FROM_EMAIL = 'webkom@hc.ntnu.no'

THUMBNAIL_DEBUG = True

SITE_ID = 1

WIKI_ACCOUNT_SIGNUP_ALLOWED = False
WIKI_ANONYMOUS_WRITE = False
WIKI_ANONYMOUS_CREATE = False

CKEDITOR_CONFIGS = {
    'news': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
    },

    'events': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
    },

    'committees': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
        'width': '100%'
    },

    'forms': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
        'width': '100%'
    },
}

DEFAULT_CONFIG = CKEDITOR_CONFIGS
GOOGLE_MAPS_API_KEY = ''
THUMBNAIL_PRESERVE_FORMAT = True
