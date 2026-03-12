import os
from xml.etree.ElementTree import ParseError
from tesoreria.models import Facturas
from gastos.models import Factura

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