import os
from xml.etree.ElementTree import ParseError
from tesoreria.models import Facturas
from gastos.models import Factura
from viaticos.models import Viaticos_Factura

import csv
from collections import defaultdict

def actualizar_facturas_compras():
    facturas = Facturas.objects.filter(uuid__isnull=True)

    for factura in facturas:
        print(f'Procesando factura ID {factura.id}')

        if factura.factura_xml and os.path.exists(factura.factura_xml.path):
            try:
                data = factura.emisor  # o la propiedad que uses para leer uuid/fecha desde XML

                if data:
                    uuid = data.get('uuid')
                    fecha_timbrado = data.get('fecha_timbrado')

                    if uuid:
                        factura.uuid = uuid
                        if fecha_timbrado:
                            factura.fecha_timbrado = fecha_timbrado
                        factura.save(update_fields=['uuid', 'fecha_timbrado'])
                        print(f'Actualizada Factura ID {factura.id}: UUID {uuid}')
                    else:
                        print(f'No se pudo obtener UUID para Factura ID {factura.id}')
                else:
                    print(f'El XML de Factura ID {factura.id} no contiene la información esperada.')

            except (ParseError, FileNotFoundError) as e:
                print(f'Error al procesar XML para Factura ID {factura.id}: {e}')
                continue

        else:
            print(f'El archivo XML no existe para Factura ID {factura.id}')
            continue

def actualizar_facturas_gastos():
    facturas = Factura.objects.filter(uuid__isnull=True)  #Gastos Filtra facturas sin UUID guardado
    for factura in facturas:
        print(factura.id)
        if factura.archivo_xml and os.path.exists(factura.archivo_xml.path):  # Verifica si el archivo XML existe
            try:
                data = factura.emisor  # Llama a la propiedad que ya tienes
                if data:  # Verifica si se pudo obtener el UUID y la fecha
                    uuid = data.get('uuid')
                    fecha_timbrado = data.get('fecha_timbrado')

                    if uuid and fecha_timbrado:
                        factura.uuid = uuid
                        factura.fecha_timbrado = fecha_timbrado
                        factura.save()
                        print(f'Actualizada Factura ID {factura.id}: UUID {uuid}')
                    else:
                        print(f'No se pudo obtener UUID y fecha para Factura ID {factura.id}')
                else:
                    print(f'El archivo XML de la factura ID {factura.id} no contiene la información esperada.')

            except (ParseError, FileNotFoundError) as e:
                print(f"Error al procesar el archivo XML para la factura ID {factura.id}: {e}")
                continue  # Salta al siguiente registro si ocurre un error

        else:
            print(f'El archivo XML no existe para la factura ID {factura.id}.')
            continue  # Salta al siguiente registro si el archivo XML no existe

def actualizar_facturas_viaticos():
    facturas = Viaticos_Factura.objects.filter(uuid__isnull=True)  #Gastos Filtra facturas sin UUID guardado
    for factura in facturas:
        print(factura.id)
        if factura.factura_xml and os.path.exists(factura.factura_xml.path):  # Verifica si el archivo XML existe
            try:
                data = factura.emisor  # Llama a la propiedad que ya tienes
                if data:  # Verifica si se pudo obtener el UUID y la fecha
                    uuid = data.get('uuid')
                    fecha_timbrado = data.get('fecha_timbrado')

                    if uuid and fecha_timbrado:
                        factura.uuid = uuid
                        factura.fecha_timbrado = fecha_timbrado
                        factura.save()
                        print(f'Actualizada Factura ID {factura.id}: UUID {uuid}')
                    else:
                        print(f'No se pudo obtener UUID y fecha para Factura ID {factura.id}')
                else:
                    print(f'El archivo XML de la factura ID {factura.id} no contiene la información esperada.')

            except (ParseError, FileNotFoundError) as e:
                print(f"Error al procesar el archivo XML para la factura ID {factura.id}: {e}")
                continue  # Salta al siguiente registro si ocurre un error

        else:
            print(f'El archivo XML no existe para la factura ID {factura.id}.')
            continue  # Salta al siguiente registro si el archivo XML no existe


def nombre_persona(obj):
    if not obj:
        return ''
    if hasattr(obj, 'staff') and obj.staff:
        staff = obj.staff
        nombre = f"{getattr(staff, 'first_name', '')} {getattr(staff, 'last_name', '')}".strip()
        return nombre or str(staff)

    nombre = f"{getattr(obj, 'first_name', '')} {getattr(obj, 'last_name', '')}".strip()
    return nombre or str(obj)


def obtener_registros_uuid():
    registros = []

    gastos = Factura.objects.select_related(
        'solicitud_gasto',
        'solicitud_gasto__staff',
    ).exclude(uuid__isnull=True).exclude(uuid='')

    for f in gastos:
        staff_gasto = getattr(f.solicitud_gasto, 'staff', None) if f.solicitud_gasto else None

        registros.append({
            'uuid': f.uuid,
            'modelo': 'Factura_Gasto',
            'id': f.id,
            'fecha_timbrado': f.fecha_timbrado,
            'xml': f.archivo_xml.name if getattr(f, 'archivo_xml', None) else '',
            'pdf': f.archivo_pdf.name if getattr(f, 'archivo_pdf', None) else '',
            'referencia': f.solicitud_gasto_id,
            'propietario': nombre_persona(staff_gasto),
            #'subido_por': str(f.subido_por) if f.subido_por else '',
        })

    compras = Facturas.objects.select_related(
        'oc',
        'oc__creada_por',
        'subido_por',
    ).exclude(uuid__isnull=True).exclude(uuid='')

    for f in compras:
        creada_por = getattr(f.oc, 'creada_por', None) if f.oc else None

        registros.append({
            'uuid': f.uuid,
            'modelo': 'Factura_Compra',
            'id': f.id,
            'fecha_timbrado': f.fecha_timbrado,
            'xml': f.factura_xml.name if getattr(f, 'factura_xml', None) else '',
            'pdf': f.factura_pdf.name if getattr(f, 'factura_pdf', None) else '',
            'referencia': f.oc_id,
            'propietario': str(creada_por) if creada_por else '',
            'subido_por': str(f.subido_por) if f.subido_por else '',
        })

    viaticos = Viaticos_Factura.objects.select_related(
        'concepto_viatico',
        'concepto_viatico__viatico',
        'concepto_viatico__viatico__staff',
        'subido_por',
    ).exclude(uuid__isnull=True).exclude(uuid='')

    for f in viaticos:
        staff_viatico = None
        if f.concepto_viatico and f.concepto_viatico.viatico:
            staff_viatico = getattr(f.concepto_viatico.viatico, 'staff', None)

        registros.append({
            'uuid': f.uuid,
            'modelo': 'Factura_Viatico',
            'id': f.id,
            'fecha_timbrado': f.fecha_timbrado,
            'xml': f.factura_xml.name if getattr(f, 'factura_xml', None) else '',
            'pdf': f.factura_pdf.name if getattr(f, 'factura_pdf', None) else '',
            'referencia': f.concepto_viatico_id,
            'propietario': nombre_persona(staff_viatico),
            'subido_por': str(f.subido_por) if f.subido_por else '',
        })

    return registros


def reporte_uuid_duplicados(ruta_csv='uuid_duplicados.csv'):
    registros = obtener_registros_uuid()

    agrupados = defaultdict(list)
    for r in registros:
        agrupados[r['uuid']].append(r)

    duplicados = {uuid: items for uuid, items in agrupados.items() if len(items) > 1}

    print(f'Total UUID duplicados encontrados: {len(duplicados)}')

    for uuid, items in duplicados.items():
        print(f'\nUUID DUPLICADO: {uuid}')
        for item in items:
            print(
                f"  - Modelo: {item['modelo']}, "
                f"ID: {item['id']}, "
                f"Referencia: {item['referencia']}, "
                f"Propietario: {item['propietario']}, "
                f"Subido por: {item['subido_por']}, "
                f"Fecha timbrado: {item['fecha_timbrado']}, "
                f"XML: {item['xml']}"
            )

    with open(ruta_csv, mode='w', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([
            'uuid',
            'modelo',
            'id',
            'referencia',
            'propietario',
            'subido_por',
            'fecha_timbrado',
            'xml',
            'pdf',
            'total_repeticiones_uuid',
        ])

        for uuid, items in duplicados.items():
            total = len(items)
            for item in items:
                writer.writerow([
                    item['uuid'],
                    item['modelo'],
                    item['id'],
                    item['referencia'],
                    item['propietario'],
                    item['subido_por'],
                    item['fecha_timbrado'],
                    item['xml'],
                    item['pdf'],
                    total,
                ])

    print(f'\nReporte generado: {ruta_csv}')