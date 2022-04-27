from msilib.schema import ListView
from re import template
from webbrowser import get
from django.shortcuts import redirect, render
import json

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


from django.http import HttpResponse,JsonResponse
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission,Group
from Usuarios.models import Usuario
# Create your views here.

from .models import  cambios, cambiosFooter
from .forms import RolForm, CambiosForm, FooterForm


def Configuracion(request):
        UserSesion=""
        try:
            if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                return render(request, "Configuracion.html", {'User':UserSesion})
        except:
            return redirect("UNR")

def Roles(request):
        UserSesion = ""
        try:
            if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                return render(request, "Roles.html", {'User':UserSesion})
        except:
            return redirect("UNR")

def Cambios(request):
    UserSesion = ""
    formulario = CambiosForm
    ListarCambios = cambios.objects.all()
    formulario2 = FooterForm
    Listarfooter =cambiosFooter.objects.all()
    try:
        if request.session:
            imagen = Usuario.objects.get(id_usuario=request.session['pk'])
            imagen = imagen.img_usuario
            if request.session['Admin'] == True:
                UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
            else:
                return redirect("SinPermisos")
    except:
        return redirect("UNR")
    contexto = {'Cambios' :ListarCambios, 'footer' :Listarfooter}
    contexto["User"]=UserSesion
    
    return render (request, "Cambios.html",contexto)

def Permisos(request):
        UserSesion=""
        try:
            if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos") 
                return render(request, "Permisos.html", {'User':UserSesion})
        except:
            return redirect("UNR")
    
class Admin(DetailView):
    model = Permission
    template_name = 'Administrador.html'
    def get(self, request,*args, **kwargs):
        context = {}
        UserSesion=""
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
        
        except:
            return redirect("UNR")

        rol = Group.objects.get(id=self.kwargs["pk"])
        permisos = rol.permissions.all()
        
        context["rol"] = rol
        context["permisos"] = permisos

        return render(request, self.template_name, context)

        

def Empleado(request):
    return render(request, "Empleado.html")

def Cliente(request):
    return render(request, "Cliente.html")


def ListarRol(request):
    UserSesion=""
    formulario=RolForm
    ListRoles = Group.objects.all()
    try:
        if request.session:
            imagen = Usuario.objects.get(id_usuario=request.session['pk'])
            imagen = imagen.img_usuario
            if request.session['Admin'] == True:
                UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
            else:
                return redirect("SinPermisos")
    except:
        pass
    contexto= {'roles':ListRoles}
    contexto["User"]=UserSesion
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
        UserSesion=""
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                return context
        except:
            return redirect("UNR")
    
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
        UserSesion=""
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                return context
        except:
            return redirect("UNR")
    
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
        UserSesion=""
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                return context
        except:
            return redirect("UNR")



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
        UserSesion=""
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                return context
        except:
            return redirect("UNR")
    

   
class listarPermisos(ListView):
    model = Permission
    template_name = 'Permisos.html'
    context_object_name = "Permisos"
    def get_context_data(self, *args, **kwargs):
        context = super(listarPermisos, self).get_context_data(**kwargs)
        UserSesion=""
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                context["grupos"] = Group.objects.all()
                return context
        except:
            return redirect("UNR")
    