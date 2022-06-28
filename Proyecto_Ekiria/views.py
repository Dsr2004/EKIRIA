#-----------------------------------------Importaciones---------------------------------------------------
from django.shortcuts import render
from Usuarios.views import *
from Usuarios.authentication_mixins import Authentication
from django.views.generic import View
from Usuarios.models import VistasDiarias
from Configuracion.models import cambios, cambiosFooter
from datetime import datetime
from Usuarios.views import *
from Ventas.models import Catalogo
from Ventas.Accesso import acceso
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
        catalogo = Catalogo.objects.all()
        catalogoLista = []
        if catalogo:
            for i in catalogo:
                tipoServicio = i.servicio_id.tipo_servicio_id.id_tipo_servicio
                if tipoServicio==1 or tipoServicio==2:
                        if len(catalogoLista) <=7-1:
                            catalogoLista.append(i)
                        else:
                            break
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        contexto = {'cambios':cambiosQueryset, 'footer':cambiosfQueryset, 'catalogo':catalogoLista}
        try:
            UserSesion = if_User(request)
            contexto["User"] = UserSesion
            return render(request, 'index.html', contexto)
        except:
            return render(request, 'index.html',contexto)
            
class menu(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'menuPrueba.html')

class ayuda(View):
    def get(self, request, *args, **kwargs):
        context ={}
        try:
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"] = UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
        except Exception as e:
            print("desde ayuda : ", e)
            
        myacceso = acceso(self.request.user)
        context["acceso"]=myacceso
        return render(request, 'ayuda.html', context)

    
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