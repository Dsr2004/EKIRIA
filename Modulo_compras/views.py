from gc import get_objects
from itertools import product
import json
from pickle import TRUE
from wsgiref.util import request_uri
from django.shortcuts import render, redirect
from Modulo_compras.forms import ProveedorForm, ComprasForm, ProductosForm, Tipo_productoForm
from .models import Proveedor, Producto, Compra, Tipo_producto
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, View
from Usuarios.models import *
from Usuarios.views import *
from Configuracion.models import cambios, cambiosFooter
from django.contrib.auth.decorators import login_required, permission_required

@login_required()
def Listproductos (request):
    UserSesion=if_admin(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    Productos=Producto.objects.all()
    producto_form=ProductosForm
    return render(request,'Productos.html',{'producto_form':producto_form , 'Productos': Productos, 'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})

@login_required()
def Listcompra(request):
    UserSesion=if_admin(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    Compras=Compra.objects.all()
    compra_form=ComprasForm
    return render(request,'compra.html',{'compra_form':compra_form , 'Compras': Compras, 'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})

@login_required()
def Listarprov(request):
    UserSesion=if_admin(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    Proveedores=Proveedor.objects.all()
    prov_form=ProveedorForm
    return render(request,'proveedores.html',{'prov_form':prov_form , 'proveedores': Proveedores, 'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})

@login_required()
def Listartp(request):
    UserSesion=if_admin(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    Tp=Tipo_producto.objects.all()
    tp_form=Tipo_productoForm
    return render(request,'tipoprod.html',{'tp_form':tp_form , 'Tp': Tp, 'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})


# class Tipoprod(View):
#     model= Tipo_producto
#     form_class=Tipo_productoForm
#     template_name='tipoprod.html'

#     def post(self,request, *args, **kwargs):  
#             prov_form = ProveedorForm(request.POST,instance=self.get_object())
#             if prov_form.is_valid():
#                 prov_form.save()
#                 return redirect('listarprov')
#             else:
#                 errors=prov_form.errors
#                 mensaje=f"{self.model.__name__} no ha sido registrado"
#                 response=JsonResponse({"errors":errors,"mensaje":mensaje})
#                 response.status_code=400
#                 return response

class Crearprod(CreateView):
    model= Producto
    form_class=ProductosForm
    template_name='modalprod/agregarprod.html'

    def post(self,request, *args, **kwargs):  
            producto_form = ProductosForm(request.POST)
            if producto_form.is_valid():
                producto_form.save()
                return redirect('listarprod')
            else:
                errors=producto_form.errors
                mensaje=f"{self.model.__name__} no ha sido registrado"
                response=JsonResponse({"errors":errors,"mensaje":mensaje})
                response.status_code=400
                return response
    def get_context_data(self, *args, **kwargs):
        context = super(Crearprod, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context

class Modificarprod(UpdateView):
    model= Producto
    form_class=ProductosForm
    template_name='modalprod/modificarprod.html'

    def post(self,request, *args, **kwargs):  
            producto_form = ProductosForm(request.POST)
            if producto_form.is_valid():
                producto_form.save()
                return redirect('listarprod')
            else:
                errors=producto_form.errors
                mensaje=f"{self.model.__name__} no ha sido registrado"
                response=JsonResponse({"errors":errors,"mensaje":mensaje})
                response.status_code=400
                return response
    def get_context_data(self, *args, **kwargs):
        context = super(Modificarprod, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context


class Creartp(CreateView):
    model=Tipo_producto
    form_class=Tipo_productoForm
    template_name='modalprod/agregartp.html'

    def post(self,request, *args, **kwargs):  
            tproducto_form = Tipo_productoForm(request.POST)
            if tproducto_form.is_valid():
                tproducto_form.save()
                return redirect('listarprod')
            else:
                errors=tproducto_form.errors
                mensaje=f"{self.model.__name__} no ha sido registrado"
                response=JsonResponse({"errors":errors,"mensaje":mensaje})
                response.status_code=400
                return response
    def get_context_data(self, *args, **kwargs):
        context = super(Creartp, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context



class Crearprov(CreateView):
    model= Proveedor
    form_class=ProveedorForm
    template_name='modalprov/agregarprov.html'

    def post(self,request, *args, **kwargs):  
            prov_form = ProveedorForm(request.POST)
            if prov_form.is_valid():
                prov_form.save()
                return redirect('listarprov')
            else:
                errors=prov_form.errors
                mensaje=f"{self.model.__name__} no ha sido registrado"
                response=JsonResponse({"errors":errors,"mensaje":mensaje})
                response.status_code=400
                return response
    def get_context_data(self, *args, **kwargs):
        context = super(Crearprov, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context
        

class Crearcompra(CreateView):
    model= Compra
    form_class=ComprasForm
    template_name='modalcomp/agregarcompra.html'

    def get(self,request,*args, **kwargs):
        producto=Producto.objects.filter(estado=True)
        form=self.form_class
        contexto={
            "productos":producto,
            "form":form
        }
        return render(request, self.template_name,contexto)

    def get_context_data(self, *args, **kwargs):
        context = super(Crearcompra, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context

    def post(self,request, *args, **kwargs): 
            if request.is_ajax():
                x=request.POST.get("datos")
                print(x)
                return JsonResponse({"s":"dfd"})

            comp_form = ComprasForm(request.POST)
            if comp_form.is_valid():
                comp_form.save()
                return redirect('listarcompra')
            else:
                errors=comp_form.errors
                mensaje=f"{self.model.__name__} no ha sido registrado"
                response=JsonResponse({"errors":errors,"mensaje":mensaje})
                response.status_code=400
                return response 

def Eliminarprov(request, id_proveedor):
    prov_form =Proveedor.objects.filter(pk=id_proveedor)
    prov_form.delete()
    return redirect('listarprov')
    # return render(request,'proveedores.html',{'prov_form':prov_form})


class modificarprov(UpdateView):
    model= Proveedor
    form_class=ProveedorForm
    template_name='modalprov/editarprov.html'

    def post(self,request, *args, **kwargs):  
            prov_form = ProveedorForm(request.POST,instance=self.get_object())
            if prov_form.is_valid():
                prov_form.save()
                return redirect('listarprov')
            else:
                errors=prov_form.errors
                mensaje=f"{self.model.__name__} no ha sido registrado"
                response=JsonResponse({"errors":errors,"mensaje":mensaje})
                response.status_code=400
                return response

    def get_context_data(self, *args, **kwargs):
        context = super(modificarprov, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context

def Actprov (request):
    pk = request.POST.get("id_proveedor")
    prov_form=Proveedor.objects.get(id_proveedor=pk)
    Proveedores=ProveedorForm(request.POST, instance=prov_form)
    if Proveedores.is_valid():
       Proveedores.save()
    return redirect('listarprov')

def cambiarestado(request):
    if request.is_ajax:
        if request.method=="POST":
            id = request.POST["estado"]
            update=Proveedor.objects.get(id_proveedor=id)
            estatus=update.estado
            if estatus==True:
                update.estado=False
                update.save()
            elif estatus==False:
                update.estado=True
                update.save()
            else:
                return redirect('listarprov')
    return JsonResponse({"kiwi":"yes"})
  
def cambiarestadoProducto(request):
    if request.is_ajax:
        if request.method=="POST":
            id = request.POST["estado"]
            update=Producto.objects.get(id_producto=id)
            estatus=update.estado
            if estatus==True:
                update.estado=False
                update.save()
            elif estatus==False:
                update.estado=True
                update.save()
            else:
                return redirect('listarprov')
    return JsonResponse({"kiwi":"yes"})
  


   
