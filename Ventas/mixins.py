from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import resolve, reverse_lazy
from django.http import HttpResponseRedirect

from Ventas.models import Cita

class ActualiarCitaMixin(object):
    def dispatch(self, request, *args, **kwargs):
        citax =Cita.objects.get(id_cita=self.kwargs["pk"])
        hoy = datetime.today()
        diaCita = citax.diaCita
        tresDias =  datetime(diaCita.year, diaCita.month, diaCita.day) - timedelta(days=3)
        if not hoy < tresDias:
            if request.session["Admin"]:
                return redirect("Ventas:listarCitas")
            elif request.session["rol"] == "Empleado":
                return redirect("Ventas:listarCitas")
            else:
                return redirect("Ventas:calendario")

        if citax.cancelado == True:
            messages.add_message(request, messages.INFO, 'Usted no puede modificar esta cita porque ha sido cancelada.')
            # url = resolve(request.path_info).url_name
            # print(request.META.get('HTTP_REFERER'))

            if request.session["Admin"]:
                return redirect("Ventas:listarCitas")
            elif request.session["rol"] == "Empleado":
                return redirect("Ventas:listarCitas")
            else:
                return redirect("Ventas:calendario")
            

            
            return redirect("Ventas:listarCitas") 
        return super().dispatch(request, *args, **kwargs)


class PoderEditarCitaMixin(object):
     def get_context_data(self, **kwargs):
        context = super( self).get_context_data(**kwargs)
        citax =Cita.objects.get(id_cita=self.kwargs["pk"]) 
        hoy = datetime.today()
        diaCita = citax.diaCita
        tresDias =  datetime(diaCita.year, diaCita.month, diaCita.day) - timedelta(days=3)
        if not hoy < tresDias:
            context[""]
        return context



class EjemploMixin(object):
    print("si entre")
    permission_required = ''
    url_redirect = None

    # def get_perms(self):
    #    if isinstance(self.permission_required,str):
    #        return(self.permission_required)
        
    #    else: return(self.permission_required)


    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('IniciarSesion')
        return self.url_redirect

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.has_perm(self.get_perms()):
    #         # print(request.user.has_perm('citasds'))
        
    #         user = request.user
    #         print(user)
        
    #         return super().dispatch(request, *args, **kwargs)
    #     return redirect(self.get_url_redirect)



""" 
mixin para lo de maria osea para saber si el usuario tiene un permiso o que chanda 
"""