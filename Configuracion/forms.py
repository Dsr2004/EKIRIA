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
            'name':forms.TextInput(attrs={"class":"form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(RolForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": "novalidate"}

class CambiosForm(forms.ModelForm):

    class Meta:
        model = cambios
        fields = '__all__'

class FooterForm(forms.ModelForm):

    class Meta:
        model = cambiosFooter
        fields = '__all__'
