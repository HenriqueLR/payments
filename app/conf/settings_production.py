from conf.settings import *

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = config.get('user_config', 'SENDGRID_API_KEY')

DATABASES = {
    'default': {
        'ENGINE': ''.join(['django.db.backends.',
            config.get('postgresql', 'DATABASE_ENGINE')]),
        'NAME': config.get('postgresql', 'DATABASE_NAME'),
        'USER': config.get('postgresql', 'DATABASE_USER'),
        'PASSWORD': config.get('postgresql', 'DATABASE_PASSWORD'),
        'HOST': config.get('postgresql', 'DATABASE_HOST'),
        'PORT': config.get('postgresql', 'DATABASE_PORT'),
    }
}