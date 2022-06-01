from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Configuracion.models import cambios, cambiosFooter
from Usuarios.models import Usuario
from Usuarios.views import if_User
from ..models import Cita, Catalogo, Servicio_Personalizado, Pedido, Servicio
from ..forms import Servicio_PersonalizadoForm
from Proyecto_Ekiria.Mixin.Mixin import PermissionDecorator, PermissionMixin

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
    queryset = Catalogo.objects.filter(estado=True)
    context_object_name = "servicios"
    template_name = "Catalogo.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Catalogo, self).get_context_data(**kwargs)
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
                return context
        except:
            return context
    
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
            request.session["carrito"]=0

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
    template_name = "Calendario.html"
    # permission_required = 'auth.can_add_group'
    # print(error)
    # @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        UserSesion=if_User(request)
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        # user = Usuario.objects.get(pk = request.session['pk'])
        # print(user.rol.permissions.set[''])
        #contexto
        citas=Cita.objects.filter(cliente_id=request.session['pk']).order_by('fecha_creacion')
      
        context={
            "User":UserSesion,
            "citas":citas, 
            'cambios':cambiosQueryset, 
            'footer':cambiosfQueryset
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
