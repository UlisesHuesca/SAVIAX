from django.contrib import admin
from .models import Cuenta, Pago

# Register your models here.
admin.site.register(Cuenta)

admin.site.register(Pago)