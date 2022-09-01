from django.db import models
from django.contrib.auth.models import User

class Tipo_perfil(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    autorizar_sol = models.BooleanField(null=True, default=False)
    autorizar_req = models.BooleanField(null=True, default=False)
    ver_sol = models.BooleanField(null=True, default=False)
    ver_req = models.BooleanField(null=True, default=False)
    crear_sol = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f'{self.nombre} - {self.autorizar_sol} - {self.autorizar_req} - {self.ver_sol - self.ver_req}'

class Distrito(models.Model):
    nombre = models.CharField(max_length=20, null=True)
    abreviado = models.CharField(max_length=3, null=True)
    def __str__(self):
        return f'{self.nombre} - {self.abreviado}'

# Create your models here.
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, upload_to='profile_images')
    tipo = models.ForeignKey(Tipo_perfil, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return f'{self.staff.username}-Profile'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url






