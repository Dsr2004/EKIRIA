from ast import If
from msilib.schema import ListView
from pyexpat import model
from re import template
import re
from webbrowser import get
import json

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.db.models import Q


from django.http import HttpResponse,JsonResponse
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission,Group
from Usuarios.models import Usuario
from Usuarios.views import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
# Create your views here.

from .models import  cambios, cambiosFooter
from .forms import RolForm, CambiosForm, FooterForm

@permission_required(['auth_permission.add_rol', 'auth_permission.change_rol', 'auth_permission.delete_rol', 'auth_permission.view_rol'])
@login_required()
def Configuracion(request):
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    UserSesion=if_admin(request)
    return render(request, "Configuracion.html", {'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})


@permission_required(['auth_permission.add_rol', 'auth_permission.change_rol', 'auth_permission.delete_rol', 'auth_permission.view_rol'])
@login_required()
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
    UserSesion=if_admin(request)
    contexto = {'Cambios' :ListarCambios, 'footer' :Listarfooter}
    contexto["User"]=UserSesion
    contexto['cambios']=cambiosQueryset
    
    return render (request, "Cambios.html",contexto)

@permission_required(['auth_permission.add_permission', 'auth_permission.change_permission', 'auth_permission.delete_permission', 'auth_permission.view_permission'])
@login_required()
def Permisos(request):
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    UserSesion=if_admin(request)
    return render(request, "Permisos.html", {'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
    

class Admin(DetailView):
    model = Permission
    template_name = 'Administrador.html'
    def get(self, request,*args, **kwargs):
        grupo = kwargs['pk']
        print(grupo)
        context = {}
        queryset = self.request.GET.get("buscar")
        UserSesion=""
        contexto= self.model.objects.all()
        if queryset:
            contexto = self.model.objects.filter(
                Q(name__icontains = queryset)
            )
        UserSesion=if_admin(self.request)
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['buscar']=contexto
        context['grupo']=grupo
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset


        rol = Group.objects.get(id=self.kwargs["pk"])
        permisos = rol.permissions.all()
        
        context["rol"] = rol
        context["permisos"] = permisos

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
    UserSesion=if_admin(request)
    contexto= {'roles':ListRoles}
    contexto["User"]=UserSesion
    contexto['cambios']=cambiosQueryset
    contexto['footer']=cambiosfQueryset
    return render(request, "Roles.html", contexto)


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

    def post(self,request, *args, **kwargs):
            if request.method == "POST":
                formulario=self.form_class(request.POST)
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
                return HttpResponse("holi")
    def get_context_data(self, *args, **kwargs):
        context = super(CreateRolView, self).get_context_data(**kwargs)
        UserSesion=if_admin(self.request)
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
        UserSesion=if_admin(self.request)
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
        UserSesion=if_admin(self.request)
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
        UserSesion=if_admin(self.request)
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
        UserSesion=if_admin(self.request)
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context["grupos"] = Group.objects.all()
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        context['buscar']=contexto
        return context



    