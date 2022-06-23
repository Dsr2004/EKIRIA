from datetime import datetime
from django.db import models
from Notificaciones.utils.models import AbstractNotificacion
from django.utils.timesince import timesince


class Notificacion(AbstractNotificacion):
    class Meta(AbstractNotificacion.Meta):
        abstract = False
        db_table = 'notificaciones'
        verbose_name ='notificacion'
        verbose_name_plural='notificiaciones'
    