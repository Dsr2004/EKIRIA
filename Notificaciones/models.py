from Notificaciones.utils.models import AbstractNotificacion


class Notificacion(AbstractNotificacion):
    class Meta(AbstractNotificacion.Meta):
        abstract = False
        db_table = 'notificaciones'
        verbose_name ='notificacion'
        verbose_name_plural='notificiaciones'
    