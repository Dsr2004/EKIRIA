from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from Configuracion.models import cambios, cambiosFooter
from Usuarios.models import Usuario
from Usuarios.views import if_User
from ..models import Cita, Catalogo, Servicio_Personalizado, Pedido, Servicio, Tipo_servicio
from ..forms import Servicio_PersonalizadoForm
from Proyecto_Ekiria.Mixin.Mixin import PermissionDecorator, PermissionMixin
from ..Accesso import acceso, accesoCatalogo
from Ventas import models
from django.contrib.auth.models import Permission,Group
def is_list_empty(list):
    if len(list) == 0:
        return True
    else:
        return False

"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administra el catalogo
<----------------------------------------------------------------->
"""

class Catalogo(ListView, PermissionMixin): 
    permission_required = ['view_catalogo']
    template_name = "Catalogo.html"
    model = models.Catalogo
    
    
        
    def get_context_data(self, *args, **kwargs):
        context = super(Catalogo, self).get_context_data(**kwargs)
        AccesoUsuario = accesoCatalogo(self.request.user)
        servicios= AccesoUsuario.DefinirServicios()
        try:
           if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                context["User"]=UserSesion
                context["User"]=UserSesion
                context['cambios']=cambiosQueryset
                context['footer']=cambiosfQueryset
                context['servicios']=servicios
                return context
            
        except:
            return context

class BuscarServicioCatalogo(View):
    def post(self, request, *args, **kwargs):
        AccesoUsuario = accesoCatalogo(self.request.user)
        serviciosx= AccesoUsuario.DefinirServicios()
        print(serviciosx)
        accion = request.POST.get("accion")
        if accion == "BuscarServicioCatalogo":
            busqueda = request.POST.get("busqueda")
            servicios = Servicio.objects.filter(nombre__icontains=busqueda)
            data=[]
            for i in servicios:
                    item = i.toJSON()
                    data.append(item)
        return JsonResponse(data, safe=False)
# @PermissionDecorator(['view_pedido', 'view pedidoItem'])    
def Carrito(request):
    try:
        cliente=Usuario.objects.get(username=request.session['username'])
        if cliente:
            pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)
            items= pedido.pedidoitem_set.all()
            serviciosx=[]
            serviciosPerx=[]
            duracion=0
            cont=0
            for i in items:
                if not i.servicio_personalizado_id == None:
                    cont+=1
            
            if cont <= 0:
                pedido.esPersonalizado = False
                pedido.save()
            cont=0
            
            for i in items:
                if not i.servicio_id ==  None:
                    duracion=duracion+i.servicio_id.duracion
                if not i.servicio_personalizado_id == None:
                    duracion=duracion+i.servicio_personalizado_id.duracion
            if items:
                for i in items:
                    if not i.servicio_id ==  None:
                        serviciosx.append(i)
                    if not i.servicio_personalizado_id == None:
                        serviciosPerx.append(i)
        
            request.session["carrito"]=pedido.get_items_carrito
            
        else:
            items=[]
            pedido={"get_total_carrito":0,"get_items_carrito":0}

        try:
            if request.session:
                    imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                    imagen = imagen.img_usuario
                    cambiosQueryset = cambios.objects.all()
                    cambiosfQueryset = cambiosFooter.objects.all()
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
        except:
                return redirect("IniciarSesion")

        contexto={"pedido":pedido,"User":UserSesion,"serviciosx":serviciosx,"serviciosPerx":serviciosPerx, "User":UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset}

        return render(request, "Carrito.html",contexto)
    except Exception as e:
        messages.add_message(request, messages.INFO, f'Ha ocurrido un error. No hay servicios registrados {str(e)}.')
        try:
            if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
        except:
            return redirect("IniciarSesion")

        contexto={"User":UserSesion,'cambios':cambiosQueryset, 'footer':cambiosfQueryset}
        return render(request, "Carrito.html",contexto)

class Calendario(TemplateView,PermissionMixin):
    permission_required = ['view_calendario']
    template_name = "Calendarios/Calendario.html"
    def get(self, request, *args, **kwargs):
        UserSesion=if_User(request)
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        citas=Cita.objects.filter(cliente_id=request.session['pk'])
        myacceso = acceso(self.request.user)
      
        context={
            "User":UserSesion,
            "citas":citas, 
            'cambios':cambiosQueryset, 
            'footer':cambiosfQueryset,
            "EsEmpleado": myacceso.esEmpleado()
        }
        
        return render(request, self.template_name, context)
    
class CalendarioEmpleado(TemplateView,PermissionMixin):
    permission_required = ['view_calendario']
    template_name = "Calendarios/CalendarioEmpleado.html"
    def get(self, request, *args, **kwargs):
        UserSesion=if_User(request)
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        citas=Cita.objects.filter(empleado_id=request.session['pk'])
        citashoy = citas.filter(diaCita=datetime.now().date()).filter(estado=1)
        print(citashoy)
        myacceso = acceso(self.request.user)
        
      
        context={
            "User":UserSesion,
            "citas":citas, 
            'cambios':cambiosQueryset, 
            'footer':cambiosfQueryset,
            "EsAdmin": myacceso.esAdministrador(),
            "citasHoy":citashoy
            
        }
        if myacceso.esEmpleado():
            return render(request, self.template_name, context)
        else:
            messages.add_message(request, messages.INFO, 'Usted no puede acceder a esta página. No tiene los permisos necesarios.')
            return redirect("Ventas:calendario")
        
        return render(request, self.template_name, context)

class CalendarioAdmin(TemplateView,PermissionMixin):
    permission_required = ['view_calendario']
    template_name = "Calendarios/CalendarioAmin.html"
    def get(self, request, *args, **kwargs):
        UserSesion=if_User(request)
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        citas=Cita.objects.filter(cliente_id=request.session['pk'])
        myacceso = acceso(self.request.user)
      
        context={
            "User":UserSesion,
            "citas":citas, 
            'cambios':cambiosQueryset, 
            'footer':cambiosfQueryset,
            "EsEmpleado": myacceso.esEmpleado()
        }
        
        return render(request, self.template_name, context)


"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se realizan las pruebas
<----------------------------------------------------------------->
"""

def ejemplo(request, id):
    consuta=Servicio.objects.filter(id_servicio=id)

def pruebas(request):
    try:
        if request.session:
            imagen = Usuario.objects.get(id_usuario=request.session['pk'])
            imagen = imagen.img_usuario
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            if request.session['Admin'] == True:
                UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
            else:
                return redirect("SinPermisos")
    except:
            return redirect("IniciarSesion")
    cont={

        "User":UserSesion,
        'cambios':cambiosQueryset, 
        'footer':cambiosfQueryset
    }
    return render(request, 'prueba.html',cont)


def correoPrueba(request):
    return  render(request, "Correo/send_email.html")
