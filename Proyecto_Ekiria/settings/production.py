from .base import *

# esta es para mysql
DEBUG = False
Domain = "ekiria.herokuapp.com"
ALLOWED_HOSTS = ['ekiria.herokuapp.com']
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ekiria_db_ekiria_tets',
#         'USER': 'ekiria_root',
#         'PASSWORD': 'Ekiria12345678.',
#         'HOST': 'mysql-ekiria.alwaysdata.net',
#         'PORT': '',
#          'OPTIONS': {
#             'init_command': 'SET default_storage_engine=INNODB',
#             'charset': 'utf8mb4',
#         }
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS  = (os.path.join(BASE_DIR, '../static/'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'../media')

LOGIN_URL = "/IniciarSesion/"
LOGIN_REDIRECT_URL = 'Inicio'
LOGOUT_REDIRECT_URL = '/'