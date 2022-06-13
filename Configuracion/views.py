from ast import If
from msilib.schema import ListView
from pyexpat import model
from re import template
import re
from webbrowser import get
import json

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db.models import Q


from django.http import HttpResponse,JsonResponse
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission,Group
from django.contrib import messages
from Usuarios.models import Usuario
from Usuarios.views import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import  cambios, cambiosFooter
from Proyecto_Ekiria.Mixin.Mixin import PermissionMixin, PermissionDecorator
from .forms import RolForm, CambiosForm, FooterForm
from Commands.seeders import PermisosCliente



@login_required()
@PermissionDecorator(['add_group', 'add_cambios', 'add_permission'])
def Configuracion(request):
    user = request.user
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    UserSesion = if_admin(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
    return render(request, "Configuracion.html",{'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})



@login_required()
@PermissionDecorator(['add_group', 'change_group', 'delete_group', 'view_group'])
def Roles(request):
    UserSesion = if_admin(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    return render(request, "Roles.html", {'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
    
@login_required()
@PermissionDecorator(['add_cambios', 'change_cambios', 'delete_cambios', 'view_cambios','add_cambiosfooter', 'change_cambiosfooter','delete_cambiosfooter','view_cambiosfooter'])
def Cambios(request):
    formulario = CambiosForm
    ListarCambios = cambios.objects.all()
    formulario2 = FooterForm
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    UserSesion = if_admin(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
    contexto = {'Cambios' :ListarCambios, 'Foter':cambiosfQueryset}
    contexto["User"]=UserSesion
    contexto['cambios']=cambiosQueryset
    contexto['footer']=cambiosfQueryset
    
    return render (request, "Cambios.html",contexto)


@login_required()
@PermissionDecorator(['add_permission', 'change_permission', 'delete_permission', 'view_permission'])
def Permisos(request):
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    UserSesion = if_admin(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
    return render(request, "Permisos.html", {'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
    

class Admin(PermissionMixin,DetailView):
    permission_required = ['add_permission','change_permission','delete_permission','view_permission',]
    model = Permission
    template_name = 'Administrador.html'
    def get(self, request,*args, **kwargs):
        grupo = kwargs['pk']
        context = {}
        queryset = self.request.GET.get("buscar")
        contexto= self.model.objects.all()
        rol = Group.objects.get(id=self.kwargs["pk"])
        permisos = rol.permissions.all()
        permisos2=rol.permissions.all()
        lista=[]
        if queryset:
            # contexto = self.model.objects.filter(
            #     Q(name__icontains = queryset)
            # )
            permisos = self.model.objects.filter(
                Q(name__icontains = queryset)
            )
        

        for i in permisos:
            id = i.codename
            lista.append(id)
        permisosexclu = Permission.objects.exclude(codename__in=lista)
        if queryset: 
            lista1 = []
            for permiso2 in permisosexclu:
                if "delete" in permiso2.codename:
                        lista1.append(permisosexclu)
            
        

        UserSesion = if_admin(request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['buscar']=contexto
        context['grupo']=grupo
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        context["rol"] = rol
        context["permisos"] = permisos
        context['permisosexclu']=permisosexclu

        return render(request, self.template_name, context)




@login_required()
@PermissionDecorator(['view_group'])
def ListarRol(request ):
    formulario=RolForm
    ListRoles = Group.objects.all()
    
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    UserSesion = if_admin(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
    contexto= {'roles':ListRoles}
    contexto["User"]=UserSesion
    contexto['cambios']=cambiosQueryset
    contexto['footer']=cambiosfQueryset
    return render(request, "Roles.html", contexto)

@PermissionDecorator(['delete_group'])
def eliminarRol(request):
    if request.method == "POST":
        id = request.POST['id']
        rol = Group.objects.get(pk = id)
        rol.delete()
        from django.contrib import messages
        messages.add_message(request, messages.SUCCESS , 'Eliminado correctamente.')
        return redirect('Roles')
    else:
        from django.contrib import messages
        messages.add_message(request, messages.INFO, 'No se puede borrar el rol, ¡ha ocurrido un error interno!')
        return redirect('Roles')
    

# def EstadoRol(request):
#     id_estado=request.POST.get("estado")
#     Object=Group.objects.get(id_rol=id_estado)
#     estado = Object.estado
#     if estado == True:
#         Object.estado = False
#         Object.save()
#         return HttpResponse('cosa')
#     elif estado == False:
#         Object.estado = True
#         Object.save()
#         return HttpResponse('cosa2')



class CreateRolView(CreateView, PermissionMixin):
    permission_required = ['add_group']
    model = Group
    form_class = RolForm
    template_name = 'CrearRol.html'

    
    def post(self, request, *args, **kwargs):
            if request.method == "POST":
                formulario=self.form_class(request.POST)
                # empleado =(request.POST['name'])
                # print(empleado)
                if formulario.is_valid():
                    rol = formulario.save()
                    roles = Group.objects.all()
                    if request.POST['tipo']=="Administrador":
                        Permisos = Permission.objects.all()
                        for permiso in Permisos:
                            rol.permissions.add(permiso)
                            rol.save()
                    if request.POST['tipo']=="Cliente":
                        PermisosCliente(rol)
                    if request.POST['tipo']=="Empleado":
                        Permisos = Permission.objects.all()
                        for permiso in Permisos:
                            rol.permissions.add(permiso)
                            rol.permissions.remove(Permission.objects.get(
                            codename='Administrador',
                            content_type=ContentType.objects.get_for_model(Usuario),
                            ))
                            rol.save()
                    return JsonResponse({"mensaje": "{self.model.__name__} Se ha creado correctamente", "errores":"No hay errores"})
                else:
                    errores=formulario.errors
                    print(formulario.is_valid())
                    mensaje=f"{self.model.__name__} No se ha creado correctamente!"
                    print(mensaje)
                    respuesta=JsonResponse({"mensaje":mensaje, "errores":errores})
                    respuesta.status_code=400
                    return respuesta
            else:
                return HttpResponse("holi")
    def get_context_data(self, *args, **kwargs):
        context = super(CreateRolView, self).get_context_data(**kwargs)
        UserSesion = if_admin(self.request)
        if UserSesion == False: 
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context

class EditarRolView(UpdateView,PermissionMixin):
    permission_required = ['change_group']
    model = Group
    form_class = RolForm
    template_name = 'EditarRol.html'
    def post(self,request, *args, **kwargs):
            if request.method == "POST":
                id_group = self.kwargs['pk']
                if id_group > 6:
                    formulario=self.form_class(request.POST, instance=self.get_object())
                    if formulario.is_valid():
                        formulario.save()
                        return JsonResponse({"mensaje": f"{self.model.__name__} Se ha creado correctamente", "errores":"No hay errores"})
                    else:
                        errores=formulario.errors
                        mensaje=f"{self.model.__name__} No se ha creado correctamente!"
                        respuesta=JsonResponse({"mensaje":mensaje, "errores":errores})
                        respuesta.status_code=400
                        return respuesta
                else:
                    from django.contrib import messages
                    messages.add_message(request, messages.INFO, 'No se puede cambiar el nombre de este rol ya que es un rol por defecto')
                    respuesta = JsonResponse({"errores":"No se puede cambiar el nombre de este rol ya que es un rol por defecto"})
                    return respuesta
            else:
                return HttpResponse("holi")

        #         else:
        #         errores=form.errors
        #         mensaje = f"{self.model.__name__} no se ha podido actualizar!"
        #         response = JsonResponse({"mensaje":mensaje, 'errors': errores})
        #         response.status_code = 400
        #         return response
        # else:
        #     return redirect("Ventas:adminVentas")
    def get_context_data(self, *args, **kwargs):
        context = super(EditarRolView, self).get_context_data(**kwargs)
        UserSesion = if_admin(self.request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context
    

class CrearCambios(View,PermissionMixin):
    permission_required = ['add_cambios', ' add_cambios_footer']
    model = cambios
    form_class = CambiosForm

    def get_object(self, queryset=None):
        obj = self.model.objects.filter(id_cambios=self.request.POST["id_cambio"]).first()
        return obj

    def post(self,request, *args, **kwargs):
        formulario=self.form_class(request.POST, instance=self.get_object())
        if formulario.is_valid():
            formulario.save()
            return JsonResponse({"mensaje": f"{self.model.__name__} Se ha creado correctamente", "errores":"No hay errores"})
        else:
            errores=formulario.errors
            mensaje=f"{self.model.__name__} No se ha creado correctamente!"
            respuesta=JsonResponse({"mensaje":mensaje, "errores":errores})
            respuesta.status_code=400
            return respuesta
    def get_context_data(self, *args, **kwargs):
        context = super(CrearCambios, self).get_context_data(**kwargs)
        UserSesion = if_admin(self.request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context
    
class CrearCambiosFooter(View,PermissionMixin):
    permission_required = ['add_cambios', ' add_cambios_footer']
    model = cambiosFooter
    form_class = FooterForm

    def get_object(self, queryset=None):
        obj = self.model.objects.filter(id_footer=self.request.POST["id_footer"]).first()
        return obj

    def post(self,request, *args, **kwargs):
        formulario=self.form_class(request.POST, instance=self.get_object())
        if formulario.is_valid():
            formulario.save()
            return JsonResponse({"mensaje": f"{self.model.__name__} Se ha creado correctamente", "errores":"No hay errores"})
        else:
            errores=formulario.errors
            mensaje=f"{self.model.__name__} No se ha creado correctamente!"
            respuesta=JsonResponse({"mensaje":mensaje, "errores":errores})
            respuesta.status_code=400
            return respuesta

    def get_context_data(self, *args, **kwargs):
        context = super(CrearCambiosFooter, self).get_context_data(**kwargs)
        UserSesion = if_admin(self.request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context



class listarPermisos(ListView,PermissionMixin):
    permission_required = ['view_permission']
    model = Permission
    template_name = 'Permisos.html'
    context_object_name="Permisos"
        
    def get_context_data(self, *args, **kwargs):
        contexto="" 
        # este es porque daña un error el contexto por no definirlo cono string
        queryset = self.request.GET.get("buscar")
        
        contexto= self.model.objects.all()
        if queryset:
            contexto = self.model.objects.filter(
                Q(name__icontains = queryset)
            )
            # return {'buscar':contexto}
            # print({'buscar':contexto} )
            # funciona

        context = super(listarPermisos, self).get_context_data(**kwargs)
        # este metodo era para intentar mostrar la consulta pero no dio
        
        UserSesion = if_admin(self.request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context["grupos"] = Group.objects.all()
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        context['buscar']=contexto
        return context



    