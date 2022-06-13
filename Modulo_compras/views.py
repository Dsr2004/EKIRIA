from gc import get_objects
import os
from itertools import product
import json
from pickle import TRUE
from wsgiref.util import request_uri
from xmlrpc.client import boolean
from django.shortcuts import render, redirect
from Modulo_compras.forms import ProveedorForm, ComprasForm, ProductosForm, Tipo_productoForm
from .models import Proveedor, Producto, Compra, Tipo_producto, HistorialCompra
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, View
from Proyecto_Ekiria import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from Usuarios.models import *
from Usuarios.views import *
from Configuracion.models import cambios, cambiosFooter
from django.contrib.auth.decorators import login_required, permission_required

@login_required()
def Listproductos (request):
    UserSesion = if_admin(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    Productos=Producto.objects.all()
    producto_form=ProductosForm
    return render(request,'Productos.html',{'producto_form':producto_form , 'Productos': Productos, 'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})

@login_required()
def Listcompra(request):
    UserSesion = if_admin(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    Compras=Compra.objects.all()
    return render(request,'compra.html',{ 'Compras': Compras, 'User':UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})

@login_required()
def Listarprov(request):
    UserSesion = if_admin(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
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
                UserSesion = if_admin(request)
                if UserSesion == False:
                    return redirect("IniciarSesion")
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
            UserSesion = if_admin(request)
            if UserSesion == False:
                return redirect("IniciarSesion")
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
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
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
                UserSesion = if_admin(request)
                if UserSesion == False:
                    return redirect("IniciarSesion")
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
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
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
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
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
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
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
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context['productos']=Producto.objects.all()
            context['proveedor']=Proveedor.objects.all()
            context['Tipo']=Tipo_producto.objects.all()
            context['form']=self.form_class
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context

    def post(self,request, *args, **kwargs): 
            if request.is_ajax():
                x=request.POST.getlist('Datos[]')
                DatosCompra = json.loads(x[0])
                Permite=True
                for datos in DatosCompra:
                    if datos['Cantidad'] == "" or datos['Precio']=="":
                        Permite=False
                if Permite==True:
                    Compra=self.model.objects.create(total = 0)
                    historial=[]
                    Total = 0
                    for datos in DatosCompra:
                        ValorNeto = int(datos['Cantidad'])*float(datos['Precio'])
                        Total = Total + ValorNeto
                        producto = Producto.objects.get(pk=int(datos['Id']))
                        producto.cantidad= producto.cantidad + int(datos['Cantidad'])
                        historial.append({"Id":Compra.pk, "Precio":float(datos['Precio']), "Cantidad":int(datos['Cantidad']), "IdProducto":producto.pk})
                        producto.save()
                        Compra.producto.add(int(datos['Id']))
                    if Total != 0 :
                        Compra.total = Total
                        Compra.save()
                        return JsonResponse({"total":Total,"historial":historial})
                    else:
                        Compra.delete()
                        data = json.dumps({'error': 'El total no puede tener un valor de 0'})
                        return HttpResponse(data, content_type="application/json", status=400)
                else:
                    data = json.dumps({'error': 'No se puede crear una compra si los campos están vacios'})
                    return HttpResponse(data, content_type="application/json", status=400)


def crearHistorial(request):
    if request.is_ajax():
        x=request.POST.getlist('historial[]')
        Historial = json.loads(x[0])
        try:
            for historial in Historial:
                HistorialCompra.objects.create(
                    precio = historial['Precio'],
                    cantidad = historial['Cantidad'],
                    compra_id = int(historial['Id']),
                    producto_id=int(historial['IdProducto']),
                )
            return JsonResponse({"success":'Success'})
        except Exception as e:
            id=None
            for historial in Historial:
                id = int(historial['Id'])
            compra = Compra.objects.get(pk = id)
            compra.producto.remove()
            compra.delete()
            data = json.dumps({'error': 'No se puedo crear el historial correctamente, por lo que la compra será eliminada'})
            return HttpResponse(data, content_type="application/json", status=400)

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


def cambiarestadoCompra(request):
    if request.is_ajax:
        if request.method=="POST":
            id = request.POST["estado"]
            update=Compra.objects.get(pk=id)
            estatus=update.estado
            historial = HistorialCompra.objects.filter(compra_id = id)
            if estatus==True:
                try:
                    update.estado=False
                    actualiza=True
                    datos =[]
                    errores = []
                    for h in historial:
                        cantidad = h.cantidad
                        producto = Producto.objects.get(pk = int(h.producto_id))
                        if producto.cantidad < cantidad:
                            actualiza = False
                            errores.append({'producto':producto.nombre})
                        else:
                            datos.append({'Id':producto.pk,'cantidad':cantidad})
                    if actualiza:
                        for data in datos:
                            producto = Producto.objects.get(pk = data['Id'])
                            producto.cantidad = producto.cantidad - int(data['cantidad'])
                            producto.save()
                        update.save()
                    else:
                        productos = ""
                        for p in errores:
                            productos = productos+p['producto']+", "
                        data = json.dumps({'error': 'No se puede cambiar el estado de esta compra porque los productos: '+str(productos)+" no tienen la cantidad suficiente para descontar la cantidad al stock"})
                        return HttpResponse(data, content_type="application/json", status=400)
                except Exception as e:
                    data = json.dumps({'error': e})
                    return HttpResponse(data, content_type="application/json", status=400)
            elif estatus==False:
                try:
                    update.estado=True
                    for h in historial:
                        cantidad = h.cantidad
                        producto = Producto.objects.get(pk = int(h.producto_id))
                        producto.cantidad = producto.cantidad + int(cantidad)
                        producto.save()
                    update.save()
                except Exception as e:
                    data = json.dumps({'error': e})
                    return HttpResponse(data, content_type="application/json", status=400)
            else:
                return redirect('listarprov')
    return JsonResponse({"kiwi":"yes"})




class verDetalleCompra(TemplateView):
    template_name = "DetalleCompra.html"
    model = Compra
    def get_context_data(self, *args, **kwargs):
        context = super(verDetalleCompra, self).get_context_data(**kwargs)
        compra = self.model.objects.get(pk = kwargs['pk'])
        productos=compra.producto.all()
        context['Compra']=compra
        context['History']=HistorialCompra.objects.filter(compra_id = kwargs['pk'])
        context['Proveedores']=Proveedor.objects.all()
        context['Productos']=productos
        UserSesion = if_admin(self.request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context
    
    def link_callback(self, uri, rel):
        sUrl = settings.local.STATIC_URL
        sRoot = settings.local.STATIC_ROOT
        mUrl = settings.local.MEDIA_URL
        mRoot = settings.local.MEDIA_ROOT
        
        if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
                return uri

        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path
        
    def post(self, request, *args, **kwargs):
        compra = self.model.objects.get(pk = kwargs['pk'])
        productos=compra.producto.all()
        context = {}
        context['Compra']=compra
        context['History']=HistorialCompra.objects.filter(compra_id = kwargs['pk'])
        context['Proveedores']=Proveedor.objects.all()
        context['Productos']=productos
        UserSesion = if_admin(self.request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        context['logo']='{}{}'.format(settings.local.STATIC_URL, 'Proyecto_Ekiria/Img/Logo Ekiria Negro 1.png')
        template = get_template("Reportes/DetalleCompra.html")
        html = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        # response['Content-Disposition']='attachment; filename="Detalle de la compra '+str(compra.fecha_creacion)+'.pdf'
        pisaStatus = pisa.CreatePDF(html, dest=response, link_callbac=self.link_callback)
        if pisaStatus.err:
            return HttpResponse('Se ha encontrado un error <pre>'+html+'</pre>')
        return response

class eliminarProductos(TemplateView):
    model=Producto
    template_name = "Funciones/RestarProductos.html"
    def get_context_data(self, *args, **kwargs):
        context = super(eliminarProductos, self).get_context_data(**kwargs)
        UserSesion = if_admin(self.request)
        if UserSesion == False:
            return redirect("IniciarSesion")
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        context['Productos']=Producto.objects.all()
        context["User"]=UserSesion
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        return context
    def post(self,request, *args, **kwargs): 
        if request.is_ajax():
            x=request.POST.getlist('Datos[]')
            DatosProductos = json.loads(x[0])
            Permite=True
            error=[]
            for datos in DatosProductos:
                if datos['Cantidad'] == "" or datos['Id']=="":
                    Permite=False
                    producto = Producto.objects.get(pk = datos['Id'])
                    error.append(producto.nombre)
            if Permite==True:
                cambiar = True
                for datos in DatosProductos:
                    producto = Producto.objects.get(pk = datos['Id'])
                    if producto.cantidad < int(datos['Cantidad']):
                        cambiar = False
                if cambiar==True: 
                    print('si')
                    for datos in DatosProductos: 
                        producto = Producto.objects.get(pk = datos['Id'])
                        producto.cantidad = producto.cantidad - int(datos['Cantidad'])
                        producto.save()
                    return JsonResponse({"success":"Succes"})
                else:
                    data = json.dumps({'error': 'No se puede realizar la acción si algunos de los productos no tiene la suficiente cantidad'})
                    return HttpResponse(data, content_type="application/json", status=400)
            else:
                data = json.dumps({'error': 'No se puede realizar la acción si alguno de los campos está vacio: '+str(error)})
                return HttpResponse(data, content_type="application/json", status=400)
                    
                        