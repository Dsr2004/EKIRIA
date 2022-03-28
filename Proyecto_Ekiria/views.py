#-----------------------------------------Importaciones---------------------------------------------------
from contextlib import redirect_stderr
from django.http import HttpResponse
from django.template import Template, Context, loader 
from django.shortcuts import render
from Usuarios.views import *
from Usuarios.authentication_mixins import Authentication
from django.views.generic import View
from rest_framework.views import APIView
from Usuarios.models import Usuario, VistasDiarias
from datetime import datetime
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
            if request.session:
                print(request.session)
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
            return render(request, 'index.html', {'User':UserSesion})
        except:
            return render(request, 'index.html')
            
class menu(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'menuPrueba.html')
    
def SinPermisos(request):
    return render(request, "SinPermisos.html")

def Noregistrado(request):
    return render(request, "NoRegistrado.html")