#-----------------------------------------Imports---------------------------------------------------
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from ast import Return
from asyncio import transports
from email import header, message
from html.entities import html5
from msilib.schema import SelfReg
from multiprocessing import context
from pyexpat import model
from pyexpat.errors import messages
from re import template
import re
from tkinter.messagebox import NO
from urllib import response
#-----------------------------------------Django---------------------------------------------------
from django.http import HttpResponseRedirect, request, HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.decorators import login_required


#-----------------------------------------Rest Framework---------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
#-----------------------------------------Serializers---------------------------------------------------
from Proyecto_Ekiria import settings
from Usuarios.Serializers.general_serializers import UsuarioTokenSerializer
from Usuarios.Serializers.general_serializers import UsuarioTokenSerializer
#-----------------------------------------Models---------------------------------------------------
from Usuarios.models import Usuario, VistasDiarias
from Ventas.models import Servicio, Pedido
from Configuracion.models import cambiosFooter, cambios
#-----------------------------------------More---------------------------------------------------
from Usuarios.authentication_mixins import Authentication
from datetime import datetime
from Usuarios.forms import Cambiar, Regitro, Editar, CustomAuthForm

#--------------------------------------Templates Loaders------------------------------------

@login_required()
def Loguot(request):
    logout(request)
    return redirect('Inicio')


def Login(request):
    Error = ""
    if request.method == "POST":
        try:
            form = CustomAuthForm(request, data=request.POST)
            if form.is_valid():
                username= form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = Usuario.objects.get(username = username)
                if user.administrador:
                    user.rol_id = 1
                    user.save()
                elif user.rol_id == 1:
                    user.rol_id = 2
                    user.save()
                usuario = authenticate(username=username, password=password)
                if usuario is not None:
                    if usuario.estado:
                        login(request, usuario)
                        request.session['username'] = usuario.username
                        request.session['rol']= usuario.rol.name
                        request.session['pk'] = usuario.id_usuario
                        request.session['Admin'] = usuario.administrador
                        # pedido, = Pedido.objects.get(cliente_id=usuario, completado=False)
                        # request.session["carrito"]=pedido.get_items_carrito
                        if 'next' in request.POST:
                            return redirect(request.POST.get('next'))
                        else:
                            return redirect("Inicio")
                    else:
                        Error = "Este Usuario se encuentra inhabilitado"
                else:
                    Error = "El Usuario o la contraseña no son correctos"
            else:
                Error = "Los datos ingresados no son correctos.\n si no tienes un usuario puedes registrarte."
        except Exception as e:
            print(e)
            
    form = CustomAuthForm()

    return render(request, "registration/login.html", {'form': form, 'message':Error})


class Register(CreateView):
    model = Usuario
    form_class = Regitro
    template_name = 'registration/Registration.html'
    success_url = reverse_lazy("IniciarSesion")

    
@login_required()
def Perfil(request):
    UserSesion = if_User(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    usuario = Usuario.objects.get(id_usuario=request.session['pk'])
    return render(request, "UserInformation/Perfil.html", {"Usuario":usuario, "User":UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})

def if_User(request):
    UserSesion=""
    if request.session:
        if request.session['pk']:
            imagen = Usuario.objects.get(id_usuario=request.session['pk'])
            imagen = imagen.img_usuario
            UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
            return UserSesion

def if_admin(request):
    UserSesion=""
    if request.session:
        if request.session['pk']:
            if request.session['Admin']:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                print(UserSesion)
                return UserSesion
            else:
                return False

@login_required()
def EditarPerfil(request):  
    template_name = "UserInformation/EditarPerfil.html"
    UserSesion = if_User(request)
    get_object = Usuario.objects.get(id_usuario=request.session['pk'])
    form = Editar(instance=get_object)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    if request.method=="POST":
        form = Editar(request.POST or None, request.FILES or None, instance=get_object)
        if form.is_valid():
            form.save()
            return redirect("Perfil")
        else:
            e=form.errors
            print(e)
            return JsonResponse({"x":e})
    return render(request, template_name, {"form":form, "User":UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
    
@login_required()
def Change(request):
    UserSesion=""
    if request.session['pk']:
        get_object = Usuario.objects.get(id_usuario=request.session['pk'])
        form = Cambiar(instance=get_object)
        imagen = Usuario.objects.get(id_usuario=request.session['pk'])
        imagen = imagen.img_usuario
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session["Admin"]}
    else: 
        return redirect("SinPermisos")
    Error = ""
    if request.method == "POST":
        try:
            oldPass = request.POST.get('passwordA')
            Pass1 = request.POST.get('password1')
            Pass2 = request.POST.get('password2')
            username= request.session['username']
            user = authenticate(username=username, password=oldPass)
            if user is not None:
                user = Usuario.objects.get(username = request.session['username'])
                if Pass1 == Pass2:
                    if Pass1 == oldPass:
                        Error = "Esta contraseña ya está en uso"
                    else:
                        if len(Pass1) >= 8:
                            if any(chr.isdigit() for chr in Pass1):
                                if any(chr.isupper() for chr in Pass1):
                                    user.set_password(Pass1)
                                    user.save()
                                    logout(request)
                                    return redirect('IniciarSesion')
                                else:
                                    Error = "La contraseña debe tener al menos una letra Mayúscula"
                            else:
                                Error = "la contraseña debe contener al menos un número"
                        else: 
                            Error = "La contraseña debe contener más de 8 digitos"
                else:
                    Error = "Las contraseñan no coinciden"
            else: 
                Error ='Contraseña incorrecta'
        except Exception as e:
            print(e)
    return render(request, 'UserInformation/ChangePassword.html', {"form":form, "User":UserSesion,'message':Error, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})

@login_required()
def Admin(request):
    UserSesion = if_admin(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    filter = "yes"
    template_name = "UsersConfiguration/UsersAdministration.html"
    if request.method=="GET":
        queryset = Usuario.objects.all()
        Servicios = Servicio.objects.all()
        Vistas = VistasDiarias.objects.get(id_dia=datetime.today().strftime('%Y-%m-%d'))
    return render(request, template_name, {"Usuario":queryset,"contexto":Servicios, "User":UserSesion, "Vistas":Vistas, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
  
class CreateUser(CreateView):
    model = Usuario
    form_class = Regitro
    template_name = 'UsersConfiguration/CreateUsers.html'
    success_url = reverse_lazy("Administracion")

    def get_context_data(self, *args, **kwargs):
        context = super(CreateUser, self).get_context_data(**kwargs)
        try:
            UserSesion = if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context

class UpdateUser(UpdateView):
    model = Usuario    
    template_name = 'UsersConfiguration/CreateUsers.html'
    form_class = Regitro
    success_url=reverse_lazy("Administracion")   
    def get_context_data(self, *args, **kwargs):
        context = super(UpdateUser, self).get_context_data(**kwargs)
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        UserSesion = if_admin(self.request)
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context

# class Notification(View):
#     template_name = 'UserInformation/Notification.html'
# class Notificacion(TemplateView):
#     template_name="UserInformation/Notification.html"

@csrf_exempt
@login_required()
def Notification(request):
    UserSesion = if_User(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    return render(request, "UserInformation/Notification.html", {"User":UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
    
def CambiarEstadoUsuario(request):
    print(request.POST)
    if request.method=="POST":
        id = request.POST["estado"]
        update=Usuario.objects.get(id_usuario=id)
        estado=update.estado
        if estado==True:
            update.estado=False
            update.save()
        elif estado==False:
            update.estado=True
            update.save()
        else:
            return redirect("Administracion")
        return HttpResponse(update)
    else:
        return JsonResponse({"x":"no"})

@api_view()
def PassR(request, token):
    messages= []
    if request.method=="GET":
        if request.user.pk is not None:
            return redirect('Inicio')
        token = token
        print(token)
    if request.method=="POST":
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 and pass2:
            if pass1 == pass2:
                if any(chr.isdigit() for chr in pass1):
                    if any(chr.isupper() for chr in pass1):
                        pass
                    else:
                        messages = "La contraseña debe tener al menos una letra Mayúscula"
                else:
                    messages ="La contraseña debe tener al menos un número"
            else:
                messages = "Las contraseñas no coinciden"
        else:
            messages = "Los campos son obligatorios"
    return render(request, "UserInformation/PasswordRecovery.html", {'message':messages})

def PassRec(request):
    messages = []
    if request.user.pk is not None:
        return redirect('Inicio')
    if request.method == "POST":
        if request.POST['email']:
            email = request.POST['email']
            if email is not None:
                user = Usuario.objects.get(email = email)
                if user.is_active:
                    try:
                        token = Token.objects.get(user=user)
                        token.delete()
                        token = Token.objects.create(user=user)

                    except:
                        Token.objects.create(user=user)
                        token = Token.objects.get(user=user)
                    try:
                        Servidor = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                        Servidor.starttls()
                        Servidor.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                        print("conexion establecida")
                        mensaje = MIMEMultipart()
                        mensaje['From'] = settings.EMAIL_HOST_USER
                        mensaje['To'] = user.email
                        mensaje['Subject'] = "Cambio de contraseña"
                        cliente = f"{str(user.nombres).capitalize()} {str(user.apellidos).capitalize()}"
                        content = render_to_string("Correo/CambioContraseñaCorreo.html",
                                                   {"cliente": cliente, "token":token.key})
                        mensaje.attach(MIMEText(content, 'html'))

                        Servidor.sendmail(settings.EMAIL_HOST_USER,
                                          user.email,
                                          mensaje.as_string())

                        print("Se envio el correo")

                    except Exception as e:
                        print(e)
            else:
                messages = "El email es requerido"

    return render(request, 'UserInformation/PasswordRecoveryEmail.html', {'message':messages})
