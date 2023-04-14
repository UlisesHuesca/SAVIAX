from django.contrib import admin
from .models import Profile, Distrito, Tipo_perfil, Banco, Almacen

# Register your models here.
admin.site.register(Profile)

admin.site.register(Distrito)

admin.site.register(Tipo_perfil)

admin.site.register(Banco)

admin.site.register(Almacen)