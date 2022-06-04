from gc import get_objects
from itertools import product
import json
from pickle import TRUE
from wsgiref.util import request_uri
from xmlrpc.client import boolean
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
    return render(request,'compra.html',{ 'Compras': Compras, 'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})

@login_required()
def Listarprov(request):
    UserSesion=if_admin(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    Proveedores=Proveedor.objects.all()
    prov_form=ProveedorForm
    return render(request,'proveedores.html',{'prov_form':prov_form , 'proveedores': Proveedores, 'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})

class Crearprod(CreateView):
    model= Producto
    form_class=ProductosForm
    template_name='Funciones/agregarprod.html'

    def post(self,request, *args, **kwargs):  
        context={}
        producto_form = self.form_class(request.POST or None)
        if producto_form.is_valid():
            nombre = producto_form.cleaned_data.get('nombre')
            proveedor = producto_form.cleaned_data.get('proveedor')
            productos = self.model.objects.all()
            boolean = None
            for producto in productos:
                if producto.nombre == nombre:
                    if producto.proveedor_id == proveedor.pk:
                        print(producto.proveedor_id)
                        boolean=False
            if boolean != False:
                producto = self.model(
                    nombre = nombre,
                    proveedor = proveedor,
                    tipo_producto = producto_form.cleaned_data.get('tipo_producto'),
                    cantidad = 0,
                )
                producto.save()
                return redirect('listarprod')
            else:
                UserSesion=if_admin(self.request)
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                tipo_producto = Tipo_producto.objects.all()
                context["User"]=UserSesion
                context['form']=producto_form
                context['cambios']=cambiosQueryset
                context['footer']=cambiosfQueryset
                context['tipo']=tipo_producto
                context['errors'] = producto_form.errors
                context['Error']="El nombre del producto ya esta relacionado a un proveedor"
                return render(request, self.template_name, context)
        else:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            tipo_producto = Tipo_producto.objects.all()
            context["User"]=UserSesion
            context['form']=producto_form
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            context['tipo']=tipo_producto
            context['errors'] = producto_form.errors
            return render(request, self.template_name, context)
    def get_context_data(self, *args, **kwargs):
        context = super(Crearprod, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            tipo_producto = Tipo_producto.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            context['tipo']=tipo_producto
            return context
        except:
            return context

class Modificarprod(UpdateView):
    model= Producto
    form_class=ProductosForm
    template_name='Funciones/agregarprod.html'

    def post(self,request, *args, **kwargs):  
            get_object = self.model.objects.get(pk=kwargs['pk'])
            producto_form = self.form_class(request.POST or None, instance=get_object)
            context={}
            if producto_form.is_valid():
                producto_form.save()
                return redirect('listarprod')
            else:
                UserSesion=if_admin(self.request)
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                tipo_producto = Tipo_producto.objects.all()
                context["User"]=UserSesion
                context['form']=producto_form
                context['cambios']=cambiosQueryset
                context['footer']=cambiosfQueryset
                context['tipo']=tipo_producto
                context['errors'] = producto_form.errors
                return render(request, self.template_name, context)
    def get_context_data(self, *args, **kwargs):
        context = super(Modificarprod, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            tipo_producto = Tipo_producto.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            context['tipo']=tipo_producto
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
                return redirect('crearprod')
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
    template_name='crearCompra.html'
    def get_context_data(self, *args, **kwargs):
        context = super(Crearcompra, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context['productos']=Producto.objects.all()
            context['proveedor']=Proveedor.objects.all()
            context['form']=self.form_class
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
        
        
class modificartp(UpdateView):
    model= Tipo_producto
    form_class=Tipo_productoForm
    template_name='modalprod/editartp.html'

    def post(self,request, *args, **kwargs):  
            get_object = self.model.objects.get(pk=kwargs['pk'])
            tp_form = self.form_class(request.POST or None, instance=get_object)
            if tp_form.is_valid():
                tp_form.save()
                return redirect('crearprod')
            else:
                errors=tp_form.errors
                mensaje=f"{self.model.__name__} no ha sido registrado"
                response=JsonResponse({"errors":errors,"mensaje":mensaje})
                response.status_code=400
                return response

    def get_context_data(self, *args, **kwargs):
        context = super(modificartp, self).get_context_data(**kwargs)
        try:
            UserSesion=if_admin(self.request)
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            context['pk']=kwargs['pk']
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
  
  
def cambiarestadoTProducto(request):
    if request.is_ajax:
        if request.method=="POST":
            id = request.POST["estado"]
            update=Tipo_producto.objects.get(pk=id)
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

class verDetalleCompra(TemplateView):
    template_name = "DetalleCompra.html"
    model = Compra
    def get_context_data(self, *args, **kwargs):
        context = super(verDetalleCompra, self).get_context_data(**kwargs)
        context['Compra']=self.model.objects.get(pk = kwargs['pk'])
        UserSesion=if_admin(self.request)
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context

