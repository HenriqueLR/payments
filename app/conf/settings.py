#coding: utf-8

"""
Django settings for app project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
from ConfigParser import RawConfigParser


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = RawConfigParser()

config.read(''.join([BASE_DIR, os.getenv('sys_arg', '')]))

SECRET_KEY = '%21sp8ltx_0nm22ttz-8h+e!4og&+cw$%i44vkn7drjt=^9*6v'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'main:home'
LOGOUT_URL = 'accounts:logout'
AUTH_USER_MODEL = 'accounts.User'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'main',
    'wallet',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = config.get('user_config', 'SENDGRID_API_KEY')

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'conf.urls'

WSGI_APPLICATION = 'conf.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': ''.join(['django.db.backends.',
            config.get('sqlite3', 'DATABASE_ENGINE')]),
        'NAME': config.get('sqlite3', 'DATABASE_NAME'),
    }
}

LANGUAGE_CODE = 'pt-br'

LANGUAGES = (
    ('pt-br', u'Português'),
    ('en', u'Inglês'),
    ('es', u'Espanhol'),
)

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = False


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR,'static_files')
STATIC_URL = '/static/'

DATE_FORMAT_US = '%Y-%m-%d'
DATE_FORMAT_BR = '%d/%m/%Y'
DATETIME_FORMAT_BR = '%d/%m/%Y %H:%M:%S'