from django.db import models

# Create your models here.



class Proveedor(models.Model):
    id_proveedor=models.AutoField("id_proveedor",primary_key=True, unique=True)
    nombre=models.CharField(max_length=20,blank=False, null=False, unique=True)
    telefono=models.CharField(max_length=10,blank=True, null=True,unique=True)
    celular=models.CharField(max_length=10,blank=False, null=False, unique=True)
    estado=models.BooleanField('estado', default=True)

    class Meta:
        verbose_name ='Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']
        db_table = 'Proveedor'

    def __str__(self):
        return self.nombre

class Tipo_producto(models.Model):
    id_tipo_producto=models.AutoField("id_tipo_producto",primary_key=True, unique=True)
    nombre=models.CharField(max_length=20,blank=False, null=False, unique=True)

    class Meta:
        verbose_name ='Tipo_producto'
        verbose_name_plural = 'Tipo_productos'
        ordering = ['nombre']
        db_table = 'Tipo_producto'

    def __str__(self):
        return self.nombre



class Producto(models.Model):
    id_producto=models.AutoField("id_producto",primary_key=True, unique=True)
    nombre=models.CharField('nombre del producto',max_length=50,blank=False, null=False)
    proveedor=models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    tipo_producto=models.ForeignKey(Tipo_producto, verbose_name="Tipo de producto",on_delete=models.CASCADE,null=False, blank=True, db_column="tipo_producto_id")
    cantidad=models.IntegerField('cantidad',blank=False, null=False)
    estado=models.BooleanField('estado', default=True)

    class Meta:
        verbose_name ='Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
        db_table = 'Producto'

    def __str__(self):
        return self.nombre

    @property

    def total(self):
        total= self.precio * self.cantidad
        return total

class Compra(models.Model):
    id_compras=models.AutoField("id_compra",primary_key=True, unique=True)
    producto=models.ManyToManyField(Producto)
    total=models.FloatField(blank=False, null=False)
    estado=models.BooleanField('estado', default=True)
    fecha_creacion=models.DateField("Fecha de Creacion", auto_now=False, auto_now_add=True)
    

    class Meta:
        verbose_name ='Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id_compras']
        db_table = 'Compra'

    def __str__(self):
        return str(self.id_compras)

class HistorialCompra(models.Model):
    id_HC=models.AutoField("id_HC",primary_key=True, unique=True)
    precio=models.FloatField(blank=False, null=False)
    cantidad=models.IntegerField(blank=False, null=False)
    compra = models.ForeignKey(Compra, null=True, blank=True, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Historial_Compra'