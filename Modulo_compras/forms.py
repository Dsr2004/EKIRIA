from tkinter import Widget
from django import forms
from Modulo_compras.models import Proveedor, Producto , Compra, Tipo_producto

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre','telefono','celular']



class Tipo_productoForm(forms.ModelForm):
    class Meta:
        model = Tipo_producto
        fields = ['nombre']
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) <= 2:
            raise forms.ValidationError('El nombre como minimo debe contener 3 letras')
        else:
            nombre = nombre.capitalize()
            return nombre
        
class ProductosForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','proveedor','tipo_producto', 'cantidad']
        widgets={
            'nombre':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre Producto *',
                    'required':'required',
                    'id':'nombre',
                }
            ),
            'proveedor': forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'proveedor',
                    'required':'requerid',
                    'autocomplete':'off',
                }
            ),
            'tipo_producto':forms.HiddenInput(
                attrs={
                    'class':'form-control',
                    'id':'tipo_producto',
                }
            ),
            'cantidad':forms.HiddenInput(
                attrs={
                    'class':'form-control',
                    'id':'cantidad',
                    'required':'requerid',
                    'autocomplete':'off',
                    'value':'0',
                }
            )
        }
    def clean_tipo_producto(self):
        tipo_producto = self.cleaned_data.get('tipo_producto')
        if tipo_producto == None:
            raise forms.ValidationError('Se necesita un tipo para el producto')
        return tipo_producto
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 4:
            raise forms.ValidationError('El nombre debe contener minimo 4 caracteres')
        return nombre


class ComprasForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['total']
        widgets={
            "total":forms.HiddenInput(
                attrs={
                    'id':'total'
                }
            )
        }