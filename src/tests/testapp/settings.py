# -*- coding: utf-8 -*-
import os

SECRET_KEY = 'dummy'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django_l10n_extensions',
    'tests.testapp',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'l10n_extensions.db'),
        # 'NAME': ':memory:',
    }
}

MEDIA_ROOT = '/tmp/django_l10n_extensions_test_media/'

MEDIA_PATH = '/media/'

ROOT_URLCONF = 'tests.testapp.urls'

DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TESTAPP_DIR = os.path.dirname(__file__)

LOCALE_PATHS = [
    os.path.join(TESTAPP_DIR, 'locale'),
]
L10N = True
LANGUAGES = (
    ('nl', u'Nederlands'),
    ('fr', u'French'),
    ('en', u'English'),
)