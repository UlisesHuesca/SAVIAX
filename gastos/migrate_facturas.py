from django.apps import apps

def migrate_facturas():
    # Obteniendo los modelos
    Solicitud_Gasto = apps.get_model('gastos', 'Solicitud_Gasto')
    Articulo_Gasto = apps.get_model('gastos', 'Articulo_Gasto')
    Factura = apps.get_model('gastos', 'Factura')

    # Iterando sobre todos los Articulo_Gasto que tengan factura_pdf y/o factura_xml
    for articulo_gasto in Articulo_Gasto.objects.filter(factura_pdf__isnull=False) | Articulo_Gasto.objects.filter(factura_xml__isnull=False):

        # Crear un diccionario para almacenar los datos de la nueva factura
        factura_data = {
            'solicitud_gasto': articulo_gasto.gasto,
            'fecha_subida': articulo_gasto.created_at
        }

        if articulo_gasto.factura_pdf:
            factura_data['archivo_pdf'] = articulo_gasto.factura_pdf

        if articulo_gasto.factura_xml:
            factura_data['archivo_xml'] = articulo_gasto.factura_xml

        # Crear el objeto Factura solo si al menos uno de los archivos (pdf o xml) existe
        if 'archivo_pdf' in factura_data or 'archivo_xml' in factura_data:
            Factura.objects.get_or_create(**factura_data)
            
        # (Opcional) Eliminar los archivos originales si se desea
        # articulo_gasto.factura_pdf.delete()
        # articulo_gasto.factura_xml.delete()
        # articulo_gasto.save()

    print("Migración completada.")

def migrar_proyecto_subproyecto():
    # Obteniendo los modelos
    #Solicitud_Gasto = apps.get_model('gastos', 'Solicitud_Gasto')
    Articulo_Gasto = apps.get_model('gastos', 'Articulo_Gasto')

    # Iterar sobre todos los Articulo_Gasto
    for articulo_gasto in Articulo_Gasto.objects.all():
        if articulo_gasto.gasto:  # Comprobando si el Articulo_Gasto tiene un objeto gasto asociado
            articulo_gasto.proyecto = articulo_gasto.gasto.proyecto
            articulo_gasto.subproyecto = articulo_gasto.gasto.subproyecto
            articulo_gasto.save()
        else:
            print(f"Articulo_Gasto con ID {articulo_gasto.id} no tiene un gasto asociado.")

    print("Migración de proyecto y subproyecto completada.")
