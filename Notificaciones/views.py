from django.shortcuts import render
from django.views.generic import View

from Usuarios.views import if_User
from Configuracion.models import cambiosFooter, cambios

from .models import Notificacion

# Create your views here.
class Notification(View):
    def get(self, request, *args, **kwargs):
        UserSesion = if_User(request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        contexto = {"User":UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset}
        notificaciones = Notificacion.objects.filter(usuario_id=request.user)
        contexto["notificaciones"] = notificaciones
        return render(request, "Notification.html", contexto)
    
