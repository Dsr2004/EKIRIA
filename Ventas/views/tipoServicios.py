"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administran los tipos de servicios
<----------------------------------------------------------------->
"""
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Permission,Group
from Proyecto_Ekiria.Mixin.Mixin import PermissionDecorator, PermissionMixin

from Ventas.forms import Tipo_servicioForm
from Ventas.models import Tipo_servicio

def get_grado():
    roles = Group.objects.all()
    grados={}
    for rol in roles:
        permisos =rol.permissions.filter(name__icontains="Puede visualizar elementos de grado").order_by('id')
        for permiso in permisos:
            grados[permiso.id]=permiso.codename
    return grados

class AgregarTipo_Servicio(CreateView):#crear
    permission_required = ['add_tipo_servicio']
    model = Tipo_servicio
    form_class = Tipo_servicioForm
    template_name = "Tipo_Servicio/Tipo_servicioAdd.html"
    
    def get_context_data(self, **kwargs):
        context = super(AgregarTipo_Servicio, self).get_context_data(**kwargs)
        context["grados"]=get_grado()
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_TipoServicio = Tipo_servicio(
                    nombre = form.cleaned_data.get('nombre'),
                    estado = form.cleaned_data.get('estado'),
                    grado_id = form.cleaned_data.get('grado_id'),
                )
                nuevo_TipoServicio.save()
                mensaje = f"{self.model.__name__} registrado correctamente"
                error = "No hay error!"
                response = JsonResponse({"mensaje":mensaje, "error":error})
                response.status_code = 201
                return response

            else:
                errores=form.errors
                mensaje = f"{self.model.__name__} no se ha podido actualizar!"
                response = JsonResponse({"mensaje":mensaje, 'errors': errores})
                response.status_code = 400
                return response
        else:
            return redirect("Ventas:adminVentas")
            
class EditarTipo_Servicio(UpdateView):#actualziar
    permission_required = ['change_tipo_servicio']
    model = Tipo_servicio
    form_class = Tipo_servicioForm
    template_name = "Tipo_Servicio/Tipo_servicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(EditarTipo_Servicio, self).get_context_data(**kwargs)
        context["grados"]=get_grado()
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f"{self.model.__name__} actualizado correctamente"
                error = "No hay error!"
                response = JsonResponse({"mensaje":mensaje, "error":error})
                response.status_code = 201
                return response
            else:
                errores=form.errors
                mensaje = f"{self.model.__name__} no se ha podido actualizar!"
                response = JsonResponse({"mensaje":mensaje, 'errors': errores})
                response.status_code = 400
                return response
        else:
            return redirect("Ventas:adminVentas")

@PermissionDecorator(['delete_tipo_servicio'])
def CambiarEstadoTipoServicio(request):
    if request.method=="POST":
        id = request.POST["estado"]
        update=Tipo_servicio.objects.get(id_tipo_servicio=id)
        estatus=update.estado
        if estatus==True:
            update.estado=False
            update.save()
        elif estatus==False:
            update.estado=True
            update.save()
        else:
            return redirect("Ventas:adminVentas")
        return HttpResponse(update)
    else:
        return redirect("Ventas:adminVentas")


class ElimininarTipoServicio(DeleteView):#eliminar
    permission_required = ['delete_tipo_servicio']
    model = Tipo_servicio
    template_name = "Tipo_Servicio/EliminarTipoServicio.html"
    success_url = reverse_lazy("Ventas:adminVentas")