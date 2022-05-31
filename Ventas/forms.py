
from crispy_forms.helper import FormHelper
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

from django import forms
from .models import Servicio, Tipo_servicio, Catalogo, Servicio_Personalizado,Cita


class ServicioForm(forms.ModelForm):
    class Meta:
        model=Servicio  
        fields=("nombre","precio","tipo_servicio_id","img_servicio","slug","descripcion", "estado","duracion")
        widgets={
            'duracion':forms.NumberInput(attrs={'class':'form-control'}),
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'tipo_servicio_id':forms.Select(attrs={"class":"form-select"}),
            'descripcion':forms.Textarea(attrs={'class':'form-control'}),
            'img_servicio':forms.FileInput(attrs={"class":"form-control",}),
            'precio':forms.NumberInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control', }),
            'estado':forms.CheckboxInput(attrs={'class':'form-check-input estadoServicioRegistro',  "style":"margin-left: -5px; height: 30px; width: 60px; margin-top: -5px"})
            
        }
    def __init__(self, *args, **kwargs):
            super(ServicioForm, self).__init__(*args, **kwargs) 
            self.fields['tipo_servicio_id'].queryset = Tipo_servicio.objects.filter(estado=True)
            self.fields['nombre'].label = False
            self.fields['precio'].label = False
            self.fields['tipo_servicio_id'].label = False
            self.fields['img_servicio'].label = False
            self.fields['slug'].label = False
            self.fields['descripcion'].label = False
            self.fields['estado'].label = False
            self.fields['duracion'].label = False
            self.fields['slug'].required = False 

        
class Tipo_servicioForm(forms.ModelForm):
    class Meta:
        model=Tipo_servicio
        fields="__all__"
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            'estado':forms.CheckboxInput(attrs={'class':'form-check-input estadoServicioRegistro',  "style":"margin-left: -5px; height: 30px; width: 60px; margin-top: -5px"})
        }
    def __init__(self, *args, **kwargs):
            super(Tipo_servicioForm, self).__init__(*args, **kwargs) 
            self.fields['nombre'].label = False
            self.fields['estado'].label = False
            

class CatalogoForm(forms.ModelForm):
    class Meta:
        model=Catalogo
        fields="__all__"
        widgets={
            'servicio_id':forms.Select(attrs={"class":"form-select"}),
            'estado':forms.CheckboxInput(attrs={'class':'form-check-input estadoServicioRegistro',  "style":"margin-left: -5px; height: 30px; width: 60px; margin-top: -5px"})
        }
    def __init__(self, *args, **kwargs):
        super(CatalogoForm, self).__init__(*args, **kwargs)
        consulta = Servicio.objects.filter(estado=True)
        self.fields['servicio_id'].queryset = consulta

class Servicio_PersonalizadoForm(forms.ModelForm):
    class Meta:
        model=Servicio_Personalizado
        fields=("tipo_servicio_id","descripcion","img_servicio","duracion")
        widgets={
            'duracion':forms.NumberInput(attrs={'class':'form-control'}),
            'tipo_servicio_id':forms.Select(attrs={"class":"form-select"}),
            'descripcion':forms.Textarea(attrs={'class':'form-control'}),
            'img_servicio':forms.FileInput(attrs={"class":"form-control"})
        }
    def __init__(self, *args, **kwargs):
        super(Servicio_PersonalizadoForm, self).__init__(*args, **kwargs) 
        self.fields['tipo_servicio_id'].queryset = Tipo_servicio.objects.filter(nombre__in=["Manicure","Pedicure","manicure","pedicure","MANICURE","PEDICURE"]).filter(estado=True)
        self.fields['img_servicio'].label = False
        self.fields['duracion'].label = False
        self.fields['descripcion'].label = False
        self.fields['duracion'].required = False
        self.fields['tipo_servicio_id'].label = False


class CitaForm(forms.ModelForm):
    class Meta:
        model= Cita
        fields =["empleado_id","diaCita","horaInicioCita","descripcion", "cliente_id", "pedido_id"]
        widgets={
            "diaCita":forms.DateInput(attrs={"class":"form-control","id":"DiaCita","type":"text","autocomplete":"off"}),
            "horaInicioCita":forms.TextInput(attrs={"class":"form-control","id":"horaInicio","type":"text","autocomplete":"off"}),
            "empleado_id":forms.Select(attrs={"class":"form-select","id":"empleado","type":"text"}),
            "descripcion":forms.Textarea(attrs={"class":"form-control","cols":"60","rows":"10"}),
           
        }
    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs) 
        self.fields['diaCita'].label = False
        self.fields['horaInicioCita'].label = False
        self.fields['empleado_id'].label = False
        self.fields['descripcion'].label = False
        self.fields['diaCita'].required = True
        self.fields['horaInicioCita'].required = True
        self.fields['empleado_id'].required = True




