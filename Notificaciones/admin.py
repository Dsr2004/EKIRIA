from Notificaciones.utils.admin import AbstractNotificacionAdmin
from django.contrib import admin
from Notificaciones.models import Notificacion

# Register your models here.

admin.site.register(Notificacion, AbstractNotificacionAdmin)