from django.contrib import admin
from Usuarios.models import Usuario
from django.contrib.auth.models import Permission

@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Permission)
