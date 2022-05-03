from Ventas.models import Cita

from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages

class ActualiarCitaMixin(object):
    def dispatch(self, request, *args, **kwargs):
        citax =Cita.objects.get(id_cita=self.kwargs["pk"])
        hoy = datetime.today()
        diaCita = citax.diaCita
        tresDias =  datetime(diaCita.year, diaCita.month, diaCita.day) - timedelta(days=3)
        if not hoy < tresDias:
            print("por dia ")
            return redirect("Ventas:listarCitas")
            

        if citax.cancelado == True:
            print("por cancelado 1")
            messages.add_message(request, messages.INFO, 'Hello world.')
            print("por cancelado 2")
            if messages:
                print(messages)

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






""" 
mixin para lo de maria osea para saber si el usuario tiene un permiso o que chanda 
"""