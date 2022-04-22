from Ventas.models import Cita

from datetime import datetime, timedelta
from django.shortcuts import render, redirect

class ActualiarCitaMixin(object):
    def dispatch(self, request, *args, **kwargs):
        citax =Cita.objects.get(id_cita=self.kwargs["pk"])
        hoy = datetime.today()
        diaCita = citax.diaCita
        tresDias =  datetime(diaCita.year, diaCita.month, diaCita.day) - timedelta(days=3)
        if not hoy < tresDias:
            return redirect("Ventas:listarCitas")
        return super().dispatch(request, *args, **kwargs)




""" 
mixin para lo de maria osea para saber si el usuario tiene un permiso o que chanda 
"""