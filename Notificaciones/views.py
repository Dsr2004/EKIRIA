from django import http
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from Usuarios.views import if_User
from Configuracion.models import cambiosFooter, cambios

from .models import Notificacion

# Create your views here.
class Notification(View):
    def get_context_data(self, **kwargs):
        context = {}
        UserSesion = if_User(self.request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"] = UserSesion
        context["cambios"] = cambiosQueryset
        context["footer"] = cambiosfQueryset
        return context
    def get(self, request, *args, **kwargs):
        contexto = self.get_context_data()
        notificaciones = Notificacion.objects.filter(usuario_id=request.user).order_by("-fecha")
        contexto["notificaciones"] = notificaciones
        return render(request, "Notification.html", contexto)
    def post(self, request, *args, **kwargs):
        contexto = self.get_context_data()
        if request.POST["tipo"] != "":
            if request.POST["tipo"] == "leido":
                notificaciones = Notificacion.objects.filter(usuario_id=request.user).filter(leido=True)
            elif request.POST["tipo"] == "Noleido":
                notificaciones = Notificacion.objects.filter(usuario_id=request.user).filter(leido=False)
        contexto["notificaciones"] = notificaciones
        return render(request, "Notification.html", contexto)
    

def BorrarNotificacion(request, pk):
    Notificacion.objects.get(id_notificacion=pk).delete()
    messages.add_message(request, messages.INFO, 'Se ha eliminado la notificación satisfactoriamente.')
    return redirect("Notify")

def CambiarEstado(request):
    if request.method == "POST":
        pk = request.POST["id"]
        notificacion =  Notificacion.objects.get(id_notificacion=pk)
        leido = notificacion.leido
        if leido == True:
            notificacion.leido = False
            messages.add_message(request, messages.INFO, 'Se ha marcado una notificación como no leida.')
        elif leido == False:
            notificacion.leido = True
            messages.add_message(request, messages.INFO, 'Se ha marcado una notificación como leida.')
        notificacion.save()
        return redirect("Notify")