import os
from xml.etree.ElementTree import ParseError
from tesoreria.models import Facturas

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