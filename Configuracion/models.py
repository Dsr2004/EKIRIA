from django.db import models

from Usuarios.models import Usuario


class cambios(models.Model):
    id_cambios =  models.AutoField(primary_key=True, unique=True)
    Color_Letra = models.CharField(max_length=20, null=False, blank=False)
    Color_Fondo = models.CharField(max_length=20, null=False, blank=False)
    tamano_Titulo = models.CharField(max_length=20, null=False, blank=False)
    tamano_Texto = models.CharField(max_length=20, null=False, blank=False)
    Tipo_Letra = models.CharField(max_length=20, null=False, blank=False)
    Texto_Mision= models.CharField(max_length=500, null=False, blank=False)
    Texto_Vision= models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        db_table = "Cambios"

    def __str__(self):
        return str(self.id_cambios)
        
class cambiosFooter(models.Model):
    id_footer = models.AutoField(primary_key=True, unique=True)
    Direccion = models.CharField(max_length=500, null=False, blank=False)
    Telefono = models.CharField(max_length=20, null=False, blank=False)
    Derechos = models.CharField(max_length=20, null=False, blank=False)
    Footer_Color_Letra = models.CharField(max_length=20, null=False, blank=False)
    Footer_Color_Fondo = models.CharField(max_length=20, null=False, blank=False)
    Footer_tamano_Titulo = models.CharField(max_length=20, null=False, blank=False)
    Footer_tamano_Texto = models.CharField(max_length=20, null=False, blank=False)
    Footer_Tipo_Letra = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = "footer"

    def __str__(self):
        return str(self.id_footer)

from django.contrib.auth.models import Group

class GroupExtensions(Group):
    class Meta:
       proxy = True

    @property
    def get_cant_users(self):
        cant = Usuario.objects.filter(rol = self).count()
        return cant
