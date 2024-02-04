from django.db import models
# De django.contrib.auth.models estamos importando el modelo de usuarios de la administration
from user.models import Distrito, Profile, Almacen
from solicitudes.models import Proyecto, Subproyecto, Operacion
#from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords
from django.core.validators import FileExtensionValidator
#from django.db.models.functions import TruncDate

# Create your models here.





class Familia(models.Model):
    nombre = models.CharField(max_length=40, null=True, unique=True)

    def __str__(self):
        return f'{self.nombre}'

class Unidad(models.Model):
    nombre = models.CharField(max_length=10, null=True, unique=True)

    def __str__(self):
        return f'{self.nombre}'

class Subfamilia(models.Model):
    nombre = models.CharField(max_length=30, null=True)
    familia = models.ForeignKey(Familia, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return f'{self.nombre}'
    
class Criticidad(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nombre}'

class Product(models.Model):
    codigo = models.CharField(max_length=6, null=True, unique=True)
    nombre = models.CharField(max_length=150, null=True, unique=True)
    unidad = models.ForeignKey(Unidad, on_delete = models.CASCADE, null=True)
    familia = models.ForeignKey(Familia, on_delete = models.CASCADE, null=True)
    subfamilia = models.ForeignKey(Subfamilia, on_delete =models.CASCADE, null=True, blank=True)
    especialista = models.BooleanField(default=False)
    iva = models.BooleanField(default=True)
    activo = models.BooleanField(default=False)
    servicio = models.BooleanField(default=False)
    gasto = models.BooleanField(default=False)
    viatico = models.BooleanField(default=False)
    baja_item = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='product_images')
    completado = models.BooleanField(default = False)
    #modificaciones para API
    critico = models.ForeignKey(Criticidad, on_delete = models.CASCADE, null=True)
    especs = models.TextField(blank=True, null=True)
    rev_calidad = models.BooleanField(default = False) 
    updated_by = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True)
    
   
    #Estas opciones de guardado de creación y actualización las voy a utilizar en todos mis modelos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))


    def __str__(self):
        return f'{self.codigo}-{self.nombre}'


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Grado_Control(models.Model):
    nombre = models.CharField(max_length=10, null=True, unique=True)
    
    def __str__(self):
        return f'{self.nombre}'
    
#Este modelo fue enteramente creado para cumplimiento con la API
class Producto_Calidad(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True)
    producto = models.OneToOneField(Product, on_delete = models.CASCADE, null=True,  related_name='producto_calidad')
    requisitos = models.TextField(blank=True, null=True)
    #criterios_aceptacion = models.TextField(blank=True, null=True)
    documental = models.BooleanField(default= False)
    inspeccion = models.BooleanField(default= False)
    cumplimiento = models.BooleanField(default= False)
    g_documental = models.ForeignKey(Grado_Control, on_delete = models.CASCADE, null=True, blank= True, related_name='documental')
    g_inspeccion = models.ForeignKey(Grado_Control, on_delete = models.CASCADE, null=True, blank=True,related_name='inspeccion')
    g_cumplimiento = models.ForeignKey(Grado_Control, on_delete = models.CASCADE, null=True, blank=True, related_name='cumplimiento')

class Products_Batch(models.Model):
    file_name = models.FileField(upload_to='product_bash', validators = [FileExtensionValidator(allowed_extensions=('csv',))])
    uploaded = models.DateField(auto_now_add=True)
    activated = models.BooleanField(default=False)


    def __str__(self):
        return f'File id:{self.id}'

class Inventario_Batch(models.Model):
    file_name = models.FileField(upload_to='product_bash', validators = [FileExtensionValidator(allowed_extensions=('csv',))])
    uploaded = models.DateField(auto_now_add=True)
    activated = models.BooleanField(default=False)


    def __str__(self):
        return f'File id:{self.id}'



class Marca(models.Model):
    nombre = models.CharField(max_length=20, null=True, unique=True)
    familia = models.ForeignKey(Familia, on_delete = models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.nombre}'





class Inventario(models.Model):
    producto = models.ForeignKey(Product, on_delete =models.CASCADE, null=True)
    distrito = models.ForeignKey(Distrito, on_delete = models.CASCADE, null=True)
    ubicacion = models.CharField(max_length=30, null=True, blank=True)
    estante = models.CharField(max_length=30, null=True, blank=True)
    marca = models.ManyToManyField(Marca, blank=True)
    almacen = models.ForeignKey(Almacen, on_delete = models.CASCADE, null=True)
    cantidad = models.DecimalField(max_digits = 14, decimal_places=2, default=0)
    cantidad_apartada = models.DecimalField(max_digits = 14, decimal_places=2, default=0)
    cantidad_entradas = models.DecimalField(max_digits = 14, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    minimo = models.PositiveIntegerField(default =0)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    comentario = models.CharField(max_length=100, null=True, blank=True)
    activo_disponible = models.BooleanField(default=False)

    class Meta:
        unique_together = ('producto', 'almacen',)


    @property
    def get_total_producto(self):
        total_inv = (self.cantidad + self.apartada) * self.price
        return total_inv

    @property
    def costo_salidas(self):
        art_ordenados = self.articulosordenados_set.all()
        total = sum([item.get_costo_salidas for item in art_ordenados])
        return total
    
    @property
    def apartada(self):
        apartados = self.articulosordenados_set.all()

        # Para cada apartado, suma los valores disponibles_true y disponibles_false
        disponibles = sum([item.articulos_disponibles for item in apartados])
           
        return disponibles
    
    @property
    def apartada_entradas(self):
        articulos = self.articulosordenados_set.all()

        #Para cada apartado, suma los valores disponibles_true y disponibles_false
        disponibles = sum([item.articulos_totales for item in articulos])
           
        return disponibles

    def __str__(self):
        return f'{self.producto}'

class Tipo_Orden(models.Model):
    tipo = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f'{self.id}:{self.tipo}'
    
class Plantilla(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creador = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name='Creador')
    modified_at = models.DateField(auto_now=True)
    modified_by = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True)
    complete = models.BooleanField(default=False)
    # otros campos que consideres necesarios

class ArticuloPlantilla(models.Model):
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE, null=True)
    cantidad = models.DecimalField(max_digits = 14, decimal_places=2, default=0)
    comentario_articulo = models.TextField(blank=True, null=True)
    comentario_plantilla = models.TextField(blank=True, null=True)
    modified_at = models.DateField(auto_now=True)
    modified_by = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True)
    # otros campos que consideres necesarios

class Order(models.Model):
    folio = models.CharField(max_length=6, null=True, unique=True)
    last_folio_number = models.IntegerField(null=True)
    staff = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name='Crea')
    proyecto = models.ForeignKey(Proyecto, on_delete = models.CASCADE, null=True)
    subproyecto = models.ForeignKey(Subproyecto, on_delete = models.CASCADE, null=True)
    distrito = models.ForeignKey(Distrito, on_delete = models.CASCADE, null=True)
    area = models.ForeignKey(Operacion, on_delete = models.CASCADE, null=True)
    #sector = models.ForeignKey(Sector, on_delete = models.CASCADE, null=True)
    superintendente = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name='intendente')
    supervisor = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name='supervisor')
    #activo = models.ForeignKey(Activo, on_delete = models.CASCADE, null=True)
    requisitar = models.BooleanField(null=True, default=False)
    requisitado = models.BooleanField(null=True, default=False)
    complete = models.BooleanField(null=True)
    tipo = models.ForeignKey(Tipo_Orden, on_delete=models.CASCADE, null=True)
    #sol_autorizada_por = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, blank=True, related_name='Autoriza')
    autorizar = models.BooleanField(null=True, default=None)
    created_at = models.DateField(null=True)
    created_at_time = models.TimeField(null=True)
    approved_at = models.DateField(null=True)
    approved_at_time = models.TimeField(null=True)
    comentario =  models.TextField(max_length=200, null=True, blank=True)
    soporte = models.FileField(blank=True, null=True, upload_to='facturas',validators=[FileExtensionValidator(['pdf'])])


    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))


    def __str__(self):
        return f'{self.id} -{self.folio} ordered by {self.staff}'
    
    @property
    def get_total_vales(self):
        salidas = self.valesalidas_set.all()
        suma =  sum([item.get_costo_vale for item in salidas])
        return suma
    
    @property
    def get_requis_compras(self):
        requisiciones = self.requis_set.all()
        suma_comprat = sum([item.get_costo_requisicion['suma_total'] for item in requisiciones])
       
        suma_pagos = sum([item.get_costo_requisicion['suma_pagos'] for item in requisiciones])
       
        return {
            'suma_comprat':suma_comprat,
           
            'suma_pagos': suma_pagos,
        }


    @property
    def get_cart_total(self):
        productos = self.articulosordenados_set.all()
        total = sum([producto.get_total for producto in productos])
        return total

    @property
    def get_cart_quantity(self):
        productos = self.articulosordenados_set.all()
        total = sum([producto.cantidad for producto in productos])
        return total

    @property
    def get_folio(self):
        return 'PL'+str(self.pk).zfill(6)


class ArticulosOrdenados(models.Model):
    producto = models.ForeignKey(Inventario, on_delete = models.CASCADE, null=True)
    orden = models.ForeignKey(Order, on_delete = models.CASCADE, null=True)
    cantidad = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.orden} - {self.producto}'
    
    @property
    def articulos_salidas(self):
        disponibles = self.articulosparasurtir_set.all()
        cantidad_salida = sum([item.cantidad_salidas for item in disponibles])
        return cantidad_salida
    
    
    
    @property
    def articulos_disponibles(self):
        disponibles = self.articulosparasurtir_set.filter(surtir=True)
        cantidad_disponible = sum([item.cantidad for item in disponibles])

        return cantidad_disponible

    @property
    def articulos_totales(self):
        articulos = self.articulosparasurtir_set.all()
        cantidad = sum([item.cantidad for item in articulos])

        return cantidad
    
    
    @property
    def get_total(self):
        total = self.producto.price * self.cantidad
        return total


class ArticulosparaSurtir(models.Model):
    articulos = models.ForeignKey(ArticulosOrdenados, on_delete = models.CASCADE, null=True)
    cantidad = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    surtir = models.BooleanField(default=False)
    cantidad_requisitar = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    comentario = models.CharField(max_length=60, null=True, blank=True)
    requisitar = models.BooleanField(null=True, default=False)
    salida = models.BooleanField(null=True, default=False)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))
    seleccionado = models.BooleanField(null=True, default=False)
    created_at = models.DateField(auto_now_add=True)
    created_at_time = models.TimeField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    @property
    def cantidad_salidas(self):
        salidas = self.salidas_set.all()
        cantidad = sum([salida.cantidad for salida in salidas])
        return cantidad

    def __str__(self):
        return f'{self.articulos} - {self.cantidad} - {self.cantidad_requisitar}'