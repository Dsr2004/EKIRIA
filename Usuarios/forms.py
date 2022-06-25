from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from Usuarios.models import Usuario
import datetime 
from dateutil.relativedelta import relativedelta


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Apodo'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Contraseña','id':'password'}))
    
class Regitro(forms.ModelForm):
    password1 = forms.CharField(label = "Contraseña", widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id':"password",
            'requerid':'requerid',
            'placeholder':'Contraseña (*)',
            'name':'password1',
        }
    ))
    password2 = forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id':"password1",
            'requerid':'requerid',
            'placeholder':'Confirmar contraseña (*)',
            'name':'password2'
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
            'estado'
        ]
        widgets = {
            'estado': forms.HiddenInput(
                attrs={
                    'value':'0',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'id':'email',
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Email (*)',
                    'name':'email',
                }
            ),
            'img_usuario': forms.FileInput(
                attrs={
                    'class':'form-control',
                    'id':'imagen',
                    'style':'display:none;',
                    'type':'file',
                    'name':'img_usuario',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'username',
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Apodo (*)',
                    'name':'username',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'nombres',
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Nombres (*)',
                    'name':'nombres',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'apellidos',
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Apellidos (*)',
                    'name':'apellidos',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'telefono',
                    'autocomplete':'off',
                    'placeholder':'Teléfono',
                    'name':'telefono',
                    'type':'number',
                }
            ),
            'celular': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'celular',
                    'required':'requerid',
                    'autocomplete':'off',
                    'type':'number',
                    'placeholder':'Celular (*)',
                    'name':'celular',
                }
            ),
            'fec_nac': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'id':'fec_nac',
                    'type':'date',
                    'required':'requerid',
                    'autocomplete':'off',
                    'style':'color:grey;',
                    'placeholder':'Fecha de nacimiento (*)',
                    'name':'fec_nac',
                }
            ),
            'tipo_documento': forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'tipo_documento',
                    'required':'requerid',
                    'autocomplete':'off',
                    'name':'tipo_documento',
                }
            ),
            'num_documento': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'num_documento',
                    'required':'requerid',
                    'autocomplete':'off',
                    'type':'number',
                    'placeholder':'Número de documento (*)',
                    'name':'num_documento',
                }
            ),
            'municipio': forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'municipio',
                    'required':'requerid',
                    'autocomplete':'off',
                    'name':'municipio',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'direccion',
                    'autocomplete':'off',
                    'placeholder':'Dirección',
                    'name':'direccion',
                }
            ),
            'cod_postal': forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'cod_postal',
                    'required':'requerid',
                    'autocomplete':'off',
                }
            ),
        }

    def clean_fec_nac(self):
        fec_nac = self.cleaned_data.get('fec_nac')
        fec_actual = datetime.datetime.now()
        edad = relativedelta(fec_actual, datetime.datetime(fec_nac.year, fec_nac.month, fec_nac.day))
        if int(edad.years) < 15:
            raise forms.ValidationError('Lo sentimos no cumples con la edad mínima para poderte registrar')
        return fec_nac

    def clean_celular(self):
        cel = self.cleaned_data.get('celular')
        if cel.isdigit() is False:
            raise  forms.ValidationError('Por favor ingresa solo números')
        if len(cel)!=10:
            raise forms.ValidationError('Por favor ingresa un número de celular correcto')
        return cel

    def clean_num_documento(self):
        num = self.cleaned_data.get('num_documento')
        if num.isdigit() is False:
            raise  forms.ValidationError('Por favor ingresa solo números')
        if len(num)!=10:
            raise forms.ValidationError('Por favor ingresa un número de celular correcto')
        return num

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
            raise forms.ValidationError('la contraseña debe contener al menos un número')
        if any(chr.isupper() for chr in password1) is False:
            raise forms.ValidationError('la contraseña debe contener al menos una Mayúscula')
        else:
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
                    'class':'form-control',
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
                    'class':'form-control',
                    'autocomplete':'off',
                }
            ),
            'celular': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'required':'requerid',
                    'autocomplete':'off',
                }
            ),
            
            'municipio': forms.Select(
                attrs={
                    'class':'form-control',
                    'required':'requerid',
                    'autocomplete':'off',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'autocomplete':'off',
                }
            ),
            'cod_postal': forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'cod_postal',
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
        
class EditUser(forms.ModelForm):
    class Meta:
        model = Usuario
        
        fields=[
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
            'rol'
        ]
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'id':'email',
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Email (*)',
                    'name':'email',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'username',
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Apodo (*)',
                    'name':'username',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'nombres',
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Nombres (*)',
                    'name':'nombres',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'apellidos',
                    'required':'requerid',
                    'autocomplete':'off',
                    'placeholder':'Apellidos (*)',
                    'name':'apellidos',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'telefono',
                    'autocomplete':'off',
                    'placeholder':'Teléfono',
                    'name':'telefono',
                    'type':'number',
                }
            ),
            'celular': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'celular',
                    'required':'requerid',
                    'autocomplete':'off',
                    'type':'number',
                    'placeholder':'Celular (*)',
                    'name':'celular',
                }
            ),
            'fec_nac': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'id':'fec_nac',
                    'type':'date',
                    'required':'requerid',
                    'autocomplete':'off',
                    'style':'color:grey;',
                    'placeholder':'Fecha de nacimiento (*)',
                    'name':'fec_nac',
                }
            ),
            'tipo_documento': forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'tipo_documento',
                    'required':'requerid',
                    'autocomplete':'off',
                    'name':'tipo_documento',
                }
            ),
            'rol': forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'rol',
                    'required':'requerid',
                    'autocomplete':'off',
                    'name':'rol',
                }
            ),
            'num_documento': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'num_documento',
                    'required':'requerid',
                    'autocomplete':'off',
                    'type':'number',
                    'placeholder':'Número de documento (*)',
                    'name':'num_documento',
                }
            ),
            'municipio': forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'municipio',
                    'required':'requerid',
                    'autocomplete':'off',
                    'name':'municipio',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'direccion',
                    'autocomplete':'off',
                    'placeholder':'Dirección',
                    'name':'direccion',
                }
            ),
            'cod_postal': forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'cod_postal',
                    'required':'requerid',
                    'autocomplete':'off',
                }
            ),
        }

    def clean_fec_nac(self):
        fec_nac = self.cleaned_data.get('fec_nac')
        fec_actual = datetime.datetime.now()
        edad = relativedelta(fec_actual, datetime.datetime(fec_nac.year, fec_nac.month, fec_nac.day))
        if int(edad.years) < 15:
            raise forms.ValidationError('Lo sentimos no cumples con la edad mínima para poderte registrar')
        return fec_nac

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if celular.isdigit() is False:
            raise  forms.ValidationError('Por favor ingresa solo números')
        if len(celular)!=10:
            raise forms.ValidationError('Por favor ingresa un número de celular correcto')
        return celular

    def clean_num_documento(self):
        num = self.cleaned_data.get('num_documento')
        if num.isdigit() is False:
            raise  forms.ValidationError('Por favor ingresa solo números')
        if len(num)!=10:
            raise forms.ValidationError('Por favor ingresa un número de celular correcto')
        return num
