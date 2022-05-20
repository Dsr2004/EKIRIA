from ast import If
from msilib.schema import ListView
from pyexpat import model
from re import template
import re
from webbrowser import get
import json

# Create your views here.
from django.http import HttpResponse
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
from Proyecto_Ekiria.Mixin.Mixin import PermissionMixin
from .forms import RolForm, CambiosForm, FooterForm



@login_required()
# @permission_required(['auth_permission.add_rol', 'auth_permission.change_rol', 'auth_permission.delete_rol', 'auth_permission.view_rol'])
def Configuracion(request):
    
    user = request.user
    # any permission check will cache the current set of permissions
    # user.has_perm('group.change_group')

    # content_type = ContentType.objects.get_for_model(Group)
    # permission = Permission.objects.get(
    #     codename='change_group',
    #     content_type=content_type,
    # )
    # permissions = Permission.objects.filter()
    # Checking the cached permission set
    # user.has_perm('group.change_group')  # False

    # Request new instance of User
    # Be aware that user.refresh_from_db() won't clear the cache.
    # user = get_object_or_404(Usuario, pk=id_user.id_usuario)

    # Permission cache is repopulated from the database
    # user.has_perm('group.change_group')  # True
    # user.user_permission.set([])
    # user.Usuario_permissions.all().values('codename')
    # user.get_group_permissions()
    # print(user.get_all_permissions())

    # if Usuario.has_perm('group.change_group'):
    #     Usuario.has_perm=True
    #     print(Usuario.has_perm)
    # else:
    #     Usuario.has_perm=False
    #     print(Usuario.has_perm)
        
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    if if_admin(request):
        UserSesion=if_admin(request)
    else: 
        return redirect('SinPermisos')
    
    return render(request, "Configuracion.html",{'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})



@login_required()
# @permission_required(['auth_permission.add_rol', 'auth_permission.change_rol', 'auth_permission.delete_rol', 'auth_permission.view_rol'])
def Roles(request):
# @permission_required(['auth_permission.add_cambios', 'auth_permission.change_cambios', 'auth_permission.delete_cambios', 'auth_permission.view_cambios','auth_permission.add_cambiosfooter', 'auth_permission.change_cambiosfooter', 'auth_permission.delete_cambiosfooter', 'auth_permission.view_cambiosfooter'])
    UserSesion=if_admin(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    return render(request, "Roles.html", {'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
    
@login_required()
def Cambios(request):
    formulario = CambiosForm
    ListarCambios = cambios.objects.all()
    formulario2 = FooterForm
    Listarfooter =cambiosFooter.objects.all()
    cambiosQueryset = cambios.objects.all()
    if if_admin(request):
        UserSesion=if_admin(request)
    else: 
        return redirect('SinPermisos')
    contexto = {'Cambios' :ListarCambios, 'footer' :Listarfooter}
    contexto["User"]=UserSesion
    contexto['cambios']=cambiosQueryset
    
    return render (request, "Cambios.html",contexto)


@login_required()
@permission_required(['auth_permission.add_permission', 'auth_permission.change_permission', 'auth_permission.delete_permission', 'auth_permission.view_permission'])
def Permisos(request):
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    UserSesion=if_admin(request)
    return render(request, "Permisos.html", {'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
    

class Admin(PermissionMixin,DetailView):
    model = Permission
    template_name = 'Administrador.html'
    def get(self, request,*args, **kwargs):
        grupo = kwargs['pk']
        print(grupo)
        context = {}
        queryset = self.request.GET.get("buscar")
        UserSesion=""
        contexto= self.model.objects.all()
        rol = Group.objects.get(id=self.kwargs["pk"])
        permisos = rol.permissions.all()
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
                        lista1.append(permiso2)
                        print(permiso2)
            # permisosexclu = lista1

        if if_admin(request):
            UserSesion=if_admin(request)
        else: 
            return redirect('SinPermisos')
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


def Empleado(request):
    return render(request, "Empleado.html")

def Cliente(request):
    return render(request, "Cliente.html")

@login_required()
def ListarRol(request):
    UserSesion=""
    formulario=RolForm
    ListRoles = Group.objects.all()
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    if if_admin(request):
        UserSesion=if_admin(request)
    else: 
        return redirect('SinPermisos')
    contexto= {'roles':ListRoles}
    contexto["User"]=UserSesion
    contexto['cambios']=cambiosQueryset
    contexto['footer']=cambiosfQueryset
    return render(request, "Roles.html", contexto)

def eliminarRol(request):
    if request.method == "POST":
        id = request.POST['id']
        rol = Group.objects.get(pk = id)
        rol.delete()
        return redirect('Roles')
    else:
        # messages. (request, messages.INFO, 'x sapapastroso inmundo')
        return redirect('Roles')
    

def EstadoRol(request):
    id_estado=request.POST.get("estado")
    Object=Group.objects.get(id_rol=id_estado)
    estado = Object.estado
    if estado == True:
        Object.estado = False
        Object.save()
        return HttpResponse('cosa')
    elif estado == False:
        Object.estado = True
        Object.save()
        return HttpResponse('cosa2')


class CreateRolView(CreateView):
    model = Group
    form_class = RolForm
    template_name = 'CrearRol.html'

    def post(self, request, *args, **kwargs):
            if request.method == "POST":
                print(request.POST)
                formulario=self.form_class(request.POST)
                if formulario.is_valid():
                    formulario.save()
                    return JsonResponse({"mensaje": f"{self.model.__name__} Se ha creado correctamente", "errores":"No hay errores"})
                else:
                    errores=formulario.errors
                    print(formulario.is_valid())
                    mensaje=f"{self.model.__name__} No se ha creado correctamente!"
                    respuesta=JsonResponse({"mensaje":mensaje, "errores":errores})
                    respuesta.status_code=400
                    return respuesta
            else:
                return HttpResponse("holi")
    def get_context_data(self, *args, **kwargs):
        context = super(CreateRolView, self).get_context_data(**kwargs)
        if if_admin(self.request):
            UserSesion=if_admin(self.request)
        else: 
            return redirect('SinPermisos')
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context
    
class CrearCambios(View):
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
            print(mensaje)
            respuesta=JsonResponse({"mensaje":mensaje, "errores":errores})
            respuesta.status_code=400
            return respuesta
    def get_context_data(self, *args, **kwargs):
        context = super(CrearCambios, self).get_context_data(**kwargs)
        if if_admin(self.request):
            UserSesion=if_admin(self.request)
        else: 
            return redirect('SinPermisos')
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context
    
class CrearCambiosFooter(View):
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
            print(mensaje)
            respuesta=JsonResponse({"mensaje":mensaje, "errores":errores})
            respuesta.status_code=400
            return respuesta

    def get_context_data(self, *args, **kwargs):
        context = super(CrearCambiosFooter, self).get_context_data(**kwargs)
        if if_admin(self.request):
            UserSesion=if_admin(self.request)
        else: 
            return redirect('SinPermisos')
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context

class EditarRolView(UpdateView):
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
                    respuesta = JsonResponse({'errores':'No se puede cambiar el nombre de este rol ya que es un rol por defecto'})
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
        if if_admin(self.request):
            UserSesion=if_admin(self.request)
        else: 
            return redirect('SinPermisos')
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context
    

   
class listarPermisos(ListView):
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
        if if_admin(self.request):
            UserSesion=if_admin(self.request)
        else: 
            return redirect('SinPermisos')
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context["grupos"] = Group.objects.all()
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        context['buscar']=contexto
        return context



    