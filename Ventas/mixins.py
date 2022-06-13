from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import resolve, reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib.auth.models import Permission,Group

from Ventas.models import Cita

from .Accesso import acceso

class ActualiarCitaMixin(object):
    def dispatch(self, request, *args, **kwargs):
        citax =Cita.objects.get(id_cita=self.kwargs["pk"])
        hoy = datetime.today()
        diaCita = citax.diaCita
        tresDias =  datetime(diaCita.year, diaCita.month, diaCita.day) - timedelta(days=3 )
        if not hoy < tresDias:
            messages.add_message(request, messages.INFO, 'Usted no puede modificar esta cita porque no cuenta con los 3 días requeridos.')
            miAcceso = acceso(request.user)
            if miAcceso.esAdministrador() or miAcceso.esEmpleado():
                return redirect("Ventas:detalleEditarCita", pk=self.kwargs["pk"])
            elif miAcceso.esCliente():
                return redirect("Ventas:calendario")

        if citax.cancelado == True:
            messages.add_message(request, messages.INFO, 'Usted no puede modificar esta cita porque ha sido cancelada.')
            if miAcceso.esAdministrador() or miAcceso.esEmpleado():
                return redirect("Ventas:detalleEditarCita", pk=self.kwargs["pk"])
            elif miAcceso.esCliente():
                return redirect("Ventas:calendario")
            return redirect("Ventas:listarCitas") 
        return super().dispatch(request, *args, **kwargs)

class ActualiarCitaClienteMixin(object):
    def dispatch(self, request, *args, **kwargs):
        citax =Cita.objects.get(id_cita=self.kwargs["pk"])
        hoy = datetime.today()
        diaCita = citax.diaCita
        tresDias =  datetime(diaCita.year, diaCita.month, diaCita.day) - timedelta(days=3)
        if not hoy <= tresDias:
            messages.add_message(request, messages.INFO, 'Usted no puede modificar esta cita porque no cuenta con los 3 días requeridos.')
            return redirect("Ventas:detalleCita", pk=self.kwargs["pk"])

        if citax.cancelado == True:
            messages.add_message(request, messages.INFO, 'Usted no puede modificar esta cita porque ha sido cancelada.')
            return redirect("Ventas:detalleCita", pk=self.kwargs["pk"])
            
        return super().dispatch(request, *args, **kwargs)






""" 
mixin para lo de maria osea para saber si el usuario tiene un permiso o que chanda 
"""