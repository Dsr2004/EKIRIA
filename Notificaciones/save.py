from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Notificacion

def saveNotify(usuario, verb, actor, direct):
    try:
        timestamp = timezone.now()
        notificacion = Notificacion(
            usuario_id = usuario,
            verbo = str(verb),
            fecha = timestamp,
            actor_content_type = ContentType.objects.get_for_model(actor),
            object_id_actor = actor.pk,
            direct = direct
            
        )
        notificacion.save()
        return True
    except:
        print("ha ocurrido un error al guardar la notificacion desde save notificaciones")
        return False
        