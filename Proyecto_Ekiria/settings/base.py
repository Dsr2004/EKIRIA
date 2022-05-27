"""
Django settings for Proyecto_Ekiria project.
Generated by 'django-admin startproject' using Django 3.2.7.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
import Crypto
import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import Proyecto_Ekiria.settings

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m8wgk*fi$u3w27#+0*rf7qja&a0=@o_kg4103z5f3du)gd_ml2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
LOCAL_APPS =[
    'Ventas',
    'Configuracion',
    'Usuarios',
    'Modulo_compras',
    'Commands'
]
THIRD_APPS =[
    'tempus_dominus',
    'crispy_forms',
    'jsonify',
    'rest_framework',
    'rest_framework.authtoken',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Proyecto_Ekiria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['Proyecto_Ekiria/Templates', 'Usuarios/Templates', 'Modulo_compras/Templates',
                 'Configuracion/Templates', 'Ventas/Templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Usuarios.context_processors.registro_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'Proyecto_Ekiria.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases



# para sqlite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

TOKEN_EXPIRED_AFTER_SECONDS = 900
Public_Key = '3082025c02010002818100c1bf62a7964d12bba2ab20139ce2c9c7a571718399350bf11b1ab3a6bb292b927b5804883e5d63fd7864514dccf06c4162dc4d31632ea64b9aefd7f04974c4bfadaab83ff23ba23e8245ee87b5bfc8dcc24086282abba4ea78a37ee454aa30f5248260ded8e8083d247e95d31a7fd34328a9e00086673775215767d62b8eab53020301000102818014be10fed0d2e6e585bb27ba51cfdf3b16404df4812b87b56ebf18c009f0ea19a04642689fb1f9e9821678b48948ad73abf4daa2d09e86ee8de38da276601fa16cc4b435fe7b68bfce20ab26030264a2b5368d1bf84d8428c583fa5a92da12afdc28c49d2a6854bf6d0b1ee4d24de9573da9e07f109d1c0825c7766c07ca9081024100d8f8549745dc4e8e5d88dd5a93ca6f791a274120410453ca965e4b4a6d7dfe5ef51a5ad68b49ce95100271257448660f2023f17c0bed8c6dae0d88d14d6578c1024100e499a3e2c23049a264860c4009f8dd649c5d7048de2b2e357589c39ac8897c4db78387c498944b97a4fcb927c2fd5757a7ea52f12ac54af389255a6c07f6f51302405ae098bdcbbb1d0430553531cd194b5b9402c11a7b610e9f9a1fe0b549eb2df2240367ecd8e68f2a8c4c198c308a6a85075746bc485ab528f37023d056f49b81024100b98210a390905d00e270817a6a5d4154472bf055c1aceae7c9054dedcab4ff6195fdafec93212ca2d7e99a5bb0f9a3aa678259628a21e6abf0ec960f3afb666f024039d52fb5ccfba193ab441c5ff723d86e2810742767232e00fe307f435aab32d8635011c7da1d79b8e9527d692921daa69ad36dd86aafa65c2427dd05838953ee'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'Usuarios.usuario'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS  = (os.path.join(BASE_DIR, '../static/'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'../media')

LOGIN_URL = "/IniciarSesion/"
LOGIN_REDIRECT_URL = 'Inicio'
LOGOUT_REDIRECT_URL = '/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# correos
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'jgallego690@misena.edu.co'

EMAIL_HOST_PASSWORD = 'xsyilkhycpnagssa'