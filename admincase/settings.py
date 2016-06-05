"""
Django settings for admincase project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-hs#yrhuxp39xj*zokvy(p(3_gj@34_lykgg76=j@c82%qw)4m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'password_reset',
    'admincase',
    'apps.clientes',
    'apps.complementos',
    'apps.complementos.locacion',
    'apps.complementos.organigrama',
    'apps.complementos.persona',
    'apps.complementos.salud',
    'apps.contactos',
    'apps.domicilios',
    'apps.personas',
    'apps.tramites',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'admincase.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates').replace('\\', '/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'admincase.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# # MySql
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'admincase',
#         'USER': 'root',
#         'PASSWORD': 'rootadmin',
#         'HOST': '',
#         'PORT': '',
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-arg'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
)


MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
MEDIA_URL = '/media/'

# PARA PRUEBA LOCAL EN CONSOLA

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ACCOUNT_ACTIVATION_DAYS = 5
# SEND_ACTIVATION_EMAIL = True

#
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587

# ESTO PARA CONFIGURAR LA RESTAURACION VIA MAIL
# EMAIL_HOST_USER = 'micorreo@gmail.com'
# EMAIL_HOST_PASSWORD = 'mipassw'
# EMAIL_USE_TLS = 1

# https://support.google.com/accounts/answer/6010255?hl=en
# ENTRAR ACA CON LA CUENTA GMAIL PARA CONFIGURA LA SEGURIDAD
# https://www.google.com/settings/security/lesssecureapps

# DEFAULT_FROM_EMAIL = 'fernandoriquelme55@gmail.com'

