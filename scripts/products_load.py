import csv
from dashboard.models import Unidad, Familia, Subfamilia, Product, Inventario
from django.db import connection
from django.contrib import messages
import pandas as pd
from django.conf import settings
import os

def run():
    fhand = open('template_products.csv')
    reader = csv.reader(fhand)
    next(reader) #Advance past the reader

    for row in reader:
        print(row)
        unidad = Unidad.objects.get(nombre = row[2])
        familia = Familia.objects.get(nombre = row[3])
        subfamilia = Subfamilia.objects.get(nombre = row[4], familia = familia)
        if unidad == None:
            messages.error('La unidad no existe dentro de la base de datos')
        elif familia == None:
            messages.error('La familia no existe dentro de la base de datos')
        elif subfamilia == None:
            messages.error('La subfamilia no existe dentro de la base de datos')
        else:
            producto = Product(codigo=row[0],nombre=row[1], unidad=unidad, familia=familia, subfamilia=subfamilia,especialista=row[5],servicio=row[6],baja_item=False)
            producto.save()

# Script para identificar posibles códigos duplicados y generar un archivo CSV
def encontrar_duplicados_inventario():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT producto_id, COUNT(*) AS duplicados
            FROM dashboard_inventario
            GROUP BY producto_id
            HAVING duplicados > 1
        ''')
        resultados = cursor.fetchall()

    data = []
    for producto_id, count in resultados:
        try:
            producto = Product.objects.get(id=producto_id)
            data.append({
                'codigo': producto.codigo,
            })
        except Product.DoesNotExist:
            pass

    if data:
        df = pd.DataFrame(data)
        root_dir = settings.BASE_DIR
        output_dir = os.path.join(root_dir, 'reportes_duplicados')
        os.makedirs(output_dir, exist_ok=True)

        file_name = 'inventario_codigos_duplicados.csv'
        file_path = os.path.join(output_dir, file_name)

        df.to_csv(file_path, index=False, encoding='utf-8', sep=',')
        print(f"Archivo generado en: {file_path}")
    else:
        print("No se encontraron códigos duplicados.")

# Script para identificar y eliminar duplicados de inventario
# Mantiene solo el registro con el ID más bajo (el primero creado)
def eliminar_duplicados_inventario():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT producto_id
            FROM dashboard_inventario
            GROUP BY producto_id
            HAVING COUNT(*) > 1
        ''')
        productos_con_duplicados = cursor.fetchall()

    for producto_id_tuple in productos_con_duplicados:
        producto_id = producto_id_tuple[0]
        duplicados = Inventario.objects.filter(producto_id=producto_id).order_by('id')

        # Mantener el primero (ID más bajo) y eliminar los demás
        inventario_a_conservar = duplicados.first()
        inventarios_a_eliminar = duplicados.exclude(id=inventario_a_conservar.id)

        eliminados = inventarios_a_eliminar.count()
        inventarios_a_eliminar.delete()

        try:
            producto = Product.objects.get(id=producto_id)
            print(f"Eliminados {eliminados} duplicados para código: {producto.codigo}")
        except Product.DoesNotExist:
            print(f"Producto con ID {producto_id} no encontrado, pero duplicados eliminados.")