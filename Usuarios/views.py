#-----------------------------------------Imports---------------------------------------------------
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

# class Login(ObtainAuthToken, TemplateView):
#     template_name = 'registration/login.html'
#     def post(self,request,*arg, **kwargs):
        # if request:
        #     login_serializer = self.serializer_class(data = request.POST , context={'request':request})
        #     print(request)
        #     if login_serializer.is_valid():
        #         user=login_serializer.validated_data['user']
        #         if user.is_active:
        #             token,created = Token.objects.get_or_create(user=user)
        #             user_serializer = UsuarioTokenSerializer(user)
        #             Client = "http://127.0.0.1:8000/"
        #             if created:
        #                 token = Token.objects.create(user = user)
        #                 # header = {'Authorization':'Token '+token.key}
        #                 # return Response(headers=header)
        #                 return HttpResponseRedirect("/")
        #             else:
        #                 all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
        #                 if all_sessions.exists():
        #                     for session in all_sessions:
        #                         session_data = session.get_decoded()
        #                         if user.id_usuario == int(session_data.get('_auth_user_id')):
        #                             session.delete()
        #                 token.delete()
        #                 token = Token.objects.create(user = user)
        #                 # credentials = 'http://127.0.0.1:8000'
        #                 # transport = HTTPTransport(credentials=credentials)
        #                 # client = Client(transports=transport)
        #                 # print(transport)
        #                 # return Response(client)
        #                 header = {'Authorization':'Token '+token.key}
        #                 return Response(headers=header)
        #                 # header = {'Authorization':'Token '+token.key}
        #                 # return Response(headers=header, template_name="index.html")
                    
                    
        #         else:
        #             return Response({'error':'Este usuario no puede iniciar sesión'}, status = status.HTTP_401_UNAUTHORIZED)
        #     else:
        #         return Response({'error':'Contraseña o Usuario incorrectos'},status=status.HTTP_400_BAD_REQUEST)


                
# class Loguot(Authentication, APIView):
#     def post(self,request,*args,**kwargs):
#         try:    
#             token = token
            
#             if token:
                
#                 user = token.user
                
#                 for i in range(2):
#                     all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
#                     if all_sessions.exists():
#                         for session in all_sessions:
#                             session_data = session.get_decoded()
#                             if user.id_usuario == int(session_data.get('_auth_user_id')):
#                                 session.delete()
                                        
#                 token.delete()
                    
#                 session_message = 'Sesiones de usuario eliminadas.'
#                 token_message = 'Token eliminado.'
#                 return Response({'token_message': token_message, 'session_message': session_message}, status = status.HTTP_200_OK)
#             return Response({'error':'No se ha encontrado un usuario con estas credenciales.'}, status = status.HTTP_400_BAD_REQUEST)
#         except :
#             return Response({'error': 'No se ha encontrado token en la petición.'}, status = status.HTTP_409_CONFLICT)

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
            
def PassR(request):
    return render(request, "UserInformation/PasswordRecovery.html")

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
                                user.set_password(Pass1)
                                user.save()
                                logout(request)
                                return redirect('IniciarSesion')
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

