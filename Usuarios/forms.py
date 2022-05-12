from unicodedata import name
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from Usuarios.models import Usuario
class Regitro(forms.ModelForm):
    password1 = forms.CharField(label = "Contraseña", widget=forms.PasswordInput(
        attrs={
            'id':"password",
            'requerid':'requerid',
            'placeholder':'Contraseña',
            'name':'password',
        }
    ))
    password2 = forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput(
        attrs={
            'id':"password1",
            'requerid':'requerid',
            'placeholder':'Confirmar contraseña',
        }
    ))
    
    class Meta:
        model = Usuario
        
        fields=[
            'img_usuario',
            'username',
            'nombres',
            'apellidos',
            'telefono',
            'celular',
            'email',
            'fec_nac',
            'tipo_documento',
            'num_documento',
            'municipio',
            'direccion',
            'cod_postal',
        ]
        widgets = {
            
            'email': forms.EmailInput(
                attrs={
                    'id':'Idate',
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Email',
                    'name':'email',
                }
            ),
            'img_usuario': forms.FileInput(
                attrs={
                    'id':'imagen',
                    'style':'display:none;',
                    'type':'file',
                    'name':'img_usuario',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Apodo',
                    'name':'username',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Nombres',
                    'name':'nombres',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Apellidos',
                    'name':'apellidos',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'autocomplete':'off',
                    'placeholder':'Telefono',
                    'name':'telefono',
                }
            ),
            'celular': forms.TextInput(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Celular',
                    'name':'celular',
                }
            ),
            'fec_nac': forms.DateInput(
                attrs={
                    'type':'date',
                    'required':'requerid',
                    'autocomplete':'off',
                    'style':'color:grey;',
                    'placeholder':'Fecha de nacimiento',
                    'name':'fec_nac',
                }
            ),
            'tipo_documento': forms.Select(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                    'name':'tipo_documento',
                }
            ),
            'num_documento': forms.TextInput(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                    'type':'number',
                    'placeholder':'Número de documento',
                    'name':'num_documento',
                }
            ),
            'municipio': forms.Select(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                    'name':'municipio',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'autocomplete':'off',
                    'placeholder':'Dirección',
                    'name':'direccion',
                }
            ),
            'cod_postal': forms.TextInput(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Codigó postal',
                    'name':'cod_postal',
                }
            ),
        }
        
    def clean_password2(self):
        """Validación de contraseña
        
        
        Metodo que valida que ambas contraseñas ingresadas sean iguales, antes de ser encriptadas, Retorna la contraseña Validada.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('La Contraseña no coincide')
        if len(password1) <= 8:
            raise forms.ValidationError('La contraseña debe contener más de 8 digitos')
        if any(chr.isdigit() for chr in password1) is False:
            raise forms.ValidationsError('la contraseña debe contener al menos un número')
        if any(chr.isupper() for chr in password1):
            raise forms.ValidationsError('la contraseña debe contener al menos una Mayúscula')
        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class Editar(forms.ModelForm):
    class Meta:
        model = Usuario
        
        fields=[
            'img_usuario',
            'telefono',
            'celular',
            'email',
            'municipio',
            'direccion',
            'cod_postal',
        ]
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'id':'Idate',
                    'required':'requerid',
                    'autocomplete':'off',
                }
            ),

            'img_usuario': forms.FileInput(
                attrs={
                    'id':'imagen',
                    'style':'display:none;',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'autocomplete':'off',
                }
            ),
            'celular': forms.TextInput(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                }
            ),
            
            'municipio': forms.Select(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'autocomplete':'off',
                }
            ),
            'cod_postal': forms.TextInput(
                attrs={
                    'required':'requerid',
                    'autocomplete':'off',
                }
            ),
        }
class Cambiar(forms.ModelForm):
    password1 = forms.CharField(label = "Contraseña", widget=forms.PasswordInput(
        attrs={
            'id':"password",
            'requerid':'requerid',
            'name':'password1',
        }
    ))
    password2 = forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput(
        attrs={
            'id':"confpassword",
            'requerid':'requerid',
            'name':'password2',
        }
    ))
    
    class Meta:
        model = Usuario
        
        fields=[
        ]
        
    def clean_password2(self):
        """Validación de contraseña
        
        
        Metodo que valida que ambas contraseñas ingresadas sean iguales, antes de ser encriptadas, Retorna la contraseña Validada.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('La Contraseña no coincide')
        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
        
class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password','id':'password'}))