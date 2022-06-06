#-----------------------------------------Importaciones---------------------------------------------------
from contextlib import redirect_stderr
from re import U
from django.http import HttpResponse
from django.template import Template, Context, loader 
from django.shortcuts import render
from Usuarios.views import *
from Usuarios.authentication_mixins import Authentication
from django.views.generic import View
from rest_framework.views import APIView
from Usuarios.models import Usuario, VistasDiarias
from Configuracion.models import cambios, cambiosFooter
from datetime import datetime
from Usuarios.views import *
#--------------------------------------Cargadores de templates------------------------------------
class Inicio(View):
    def get(self, request, *args, **kwargs):  
        try:
            Vista = VistasDiarias.objects.get(id_dia=datetime.today().strftime('%Y-%m-%d')) 
            Vista.Contador = Vista.Contador + 1
            Vista.save()
        except:
            Vistas = VistasDiarias.objects.create(id_dia=datetime.today().strftime('%Y-%m-%d'))
            Vista = VistasDiarias.objects.get(id_dia=datetime.today().strftime('%Y-%m-%d')) 
            Vista.Contador = Vista.Contador + 1
            Vista.save()
        try:
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            UserSesion = if_User(request)
            return render(request, 'index.html', {'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
        except:
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            return render(request, 'index.html',{'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
            
class menu(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'menuPrueba.html')
    
def SinPermisos(request):
    return render(request, "SinPermisos.html")

def Noregistrado(request):
    return render(request, "NoRegistrado.html")



#------------------------------------------Errors HTTPS STATUS------------------------------------
class Error404(TemplateView):
    template_name="Https/Errors/404.html"
    
class Error500(TemplateView):
    template_name="https/Errors/500.html"
    
    @classmethod
    def as_error_view(cls):
        v=cls.as_view()
        def view(request):
            r = v(request)
            r.render()
            return r
        return view
def Errors(request):
    return render(request, 'Https/Errors.html')