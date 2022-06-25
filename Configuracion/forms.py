from dataclasses import fields
from django import forms
from .models import cambios,cambiosFooter
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import Group

class RolForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        widgets={
            'name':forms.TextInput(attrs={"class":"form-control" }),
            
        }

    def __init__(self, *args, **kwargs):
        super(RolForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": "novalidate"}
        self.fields['name'].label=False

    def clean_name(self):  
        name = self.cleaned_data.get('name')
        if len(name)<4:
            raise forms.ValidationError('Este campo requiere más de 4 digitos')
        elif len(name)>20:
            raise forms.ValidationError('El maximo de este campo es de 20 digitos')
        return name
class CambiosForm(forms.ModelForm):

    class Meta:
        model = cambios
        fields = '__all__'

class FooterForm(forms.ModelForm):

    class Meta:
        model = cambiosFooter
        fields = '__all__'
