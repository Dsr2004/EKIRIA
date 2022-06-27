#contenttpes
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


#timezone
from django.utils import timezone

# load model 
from swapper import load_model

#signals
from Notificaciones.signals import notificar

#modelos
from Usuarios.models import Usuario

#django
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.db import models

class NotificacionQuerySet(models.QuerySet):
    def leido(self):
        #retorna las notificaciones que han sido leidas
        return self.filter(leido=True)
        
    def no_leido(self):
        #retorna las notificaciones que no han sido leidas
        return self.filter(leido=False)
        
    def marcar_todas_leidas(self, usuario_id=None):
        #marca todas las notificaciones como leidas del usuario
        consulta = self.leido(False)
        if usuario_id:
            consulta = consulta.filter(usuario_id=usuario_id)
        return consulta.update(leido=True)
    
    def marcar_todas_no_leidas(self, usuario_id=None):
        #marca todas las notificaciones como no leidas del usuario
        consulta = self.leido(True)
        if usuario_id:
            consulta = consulta.filter(usuario_id=usuario_id)
        return consulta.update(leido=False)
    
class AbstractNotificacionManager(models.Manager):
    #cambios la propiedad queryset para que sea una clase administradora de notificaciones
    def get_queryset(self):
        return self.NotificacionQuerySet(self.model, using=self._db) #mando el modelo y que use mi base de datos
    
class AbstractNotificacion(models.Model):
   
    id_notificacion = models.AutoField(primary_key=True)
    verbo = models.CharField(max_length=220) #lo que se va a mostrar en la notificacion
    fecha = models.DateTimeField(default=timezone.now, db_index=True) #fecha y hora de la notificacion
    usuario_id = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE, related_name="notificaciones") #usuario que recibe la notificacion
    leido = models.BooleanField(default=False) #si la notificacion ha sido leida o no
    direct = models.CharField(max_length = 200, null=True, blank=True)

    actor_content_type = models.ForeignKey(ContentType, related_name="notificar_actor", on_delete=models.CASCADE)
    object_id_actor = models.PositiveIntegerField()
    actor = GenericForeignKey("actor_content_type", "object_id_actor")

    objects: NotificacionQuerySet.as_manager() #query set para filtrar las notificaciones, segun su estado en este caso leidas


    class Meta:
        abstract = True
        
def notificaciones_signals(verbo, **kwargs):
    #crea una instancia de mi notificacion tras una llamada del signal
    usuario = kwargs.pop('usuario_id')
    timestamp = kwargs.pop('tiempo', timezone.now()) 
    Notificacion = load_model('Notificaciones', 'Notificacion')
    actor = kwargs.pop('sender')
    direct = kwargs.pop('direct')
    
    if  isinstance(usuario, Group):
        usuarios = usuario.user_set.all()
    elif isinstance(usuario, (QuerySet, list)):
        usuarios = usuario
    else:
        usuarios = [usuario]
        
        
    nueva_notificacion = []
    for usuario in usuarios:
        notificacion = Notificacion(
            usuario_id = usuario,
            verbo = str(verbo),
            fecha = timestamp,
            actor_content_type = ContentType.objects.get_for_model(actor),
            object_id_actor = actor.pk,
            direct = direct
            
        )
        notificacion.save()
        nueva_notificacion.append(notificacion)
    return nueva_notificacion

notificar.connect(notificaciones_signals, dispatch_uid='Notifiacioes.models.Notificacion')