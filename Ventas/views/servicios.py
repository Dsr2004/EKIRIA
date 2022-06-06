"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administran los servicios
<----------------------------------------------------------------->
"""
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from Configuracion.models import cambios, cambiosFooter
from Usuarios.models import Usuario
from Ventas.forms import ServicioForm
from Ventas.models import Servicio, Catalogo
from Proyecto_Ekiria.Mixin.Mixin import PermissionDecorator, PermissionMixin


class AgregarServicio(CreateView,PermissionMixin):#crear
    permission_required = ['add_servicio']
    model = Servicio
    form_class = ServicioForm
    template_name = "AgregarServicio.html"
    success_url = reverse_lazy('Ventas:listarServicios')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                    context["User"]=UserSesion
                    context['cambios']=cambiosQueryset
                    context['footer']=cambiosfQueryset
                else:
                    return redirect("SinPermisos")
        except:
            return redirect("IniciarSesion")
        return context
    def form_valid(self, form, **kwargs):
        objeto=form.save()
        if objeto.estado == True:
            ServicioToCatalogo = Catalogo.objects.create(servicio_id=objeto)
            ServicioToCatalogo.save()
        objeto.save()
        return redirect("Ventas:listarServicios")

class EditarServicio(UpdateView,PermissionMixin):#actualizar
    permission_required = ['change_servicio']
    model = Servicio
    form_class = ServicioForm
    template_name = "EditarServicio.html" 
    success_url = reverse_lazy('Ventas:listarServicios')
    
    def get_context_data(self, *args, **kwargs):
        context = super(EditarServicio, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                    context["User"]=UserSesion
                    context['cambios']=cambiosQueryset
                    context['footer']=cambiosfQueryset
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                context['cambios']=cambiosQueryset
                context['footer']=cambiosfQueryset
                return context
        except:
            return context
       
    def form_valid(self, form, **kwargs):
        objeto=form.save()
        if objeto.estado == False:
            QuitarServicioToCatalogo = Catalogo.objects.filter(servicio_id=objeto).delete()
        elif objeto.estado == True:
            ServicioToCatalogo = Catalogo.objects.create(servicio_id=objeto)
            ServicioToCatalogo.save()
        objeto.save()
        return redirect("Ventas:listarServicios")

class ListarServicio(ListView,PermissionMixin):#listar
    permission_required = ['view_servicio']
    queryset = Servicio.objects.all()
    context_object_name = "servicios"
    template_name = "ListarServicios.html"
  
    def get_context_data(self, *args, **kwargs):
        context = super(ListarServicio, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                    context["User"]=UserSesion
                    context['cambios']=cambiosQueryset
                    context['footer']=cambiosfQueryset
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                context['footer']=cambiosfQueryset
                context['cambios']=cambiosQueryset
                return context
        except:
            return redirect("IniciarSesion")

class ServicioDetalle(DetailView,PermissionMixin):#detalle
    permission_required = ['view_servicio']
    queryset = Servicio.objects.all()
    context_object_name = "DetailSs"
    template_name = "Catalogo/Detalle_Servicio.html"

@PermissionDecorator(['delete_servicio'])
def CambiarEstadoServicio(request):
    if request.method == "POST":
        id = request.POST["estado"]
        update=Servicio.objects.get(id_servicio=id)
        estatus=update.estado
        if estatus==True:
            update.estado=False
            QuitarServicioToCatalogo = Catalogo.objects.filter(servicio_id=update).delete()
            update.save()
        elif estatus==False:
            update.estado=True
            update.save()
            ServicioToCatalogo = Catalogo.objects.create(servicio_id=update)
            ServicioToCatalogo.save()
        else:
            return redirect("Ventas:listarServicios")
        return HttpResponse(update)
    else:
        return redirect("Ventas:listarServicios")
