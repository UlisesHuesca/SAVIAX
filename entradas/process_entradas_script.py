# process_entradas_script.py

# Importando los modelos desde la app "compras"
from compras.models import Compra, ArticuloComprado

# Aquí va el código para procesar las compras y artículos:

def procesar_entradas():
    compras = Compra.objects.filter(autorizado2=True, entrada_completa = False)

    # Contador de OC modificadas y lista para almacenar las IDs
    oc_modificadas = 0
    ids_modificadas = []


    for compra in compras:
    
        articulos = ArticuloComprado.objects.filter(oc=compra)
    
        for articulo in articulos:
            if articulo.cantidad_pendiente == 0:
                articulo.entrada_completa = True
                articulo.seleccionado = True
                articulo.save()
    
        num_art_entregados = articulos.filter(entrada_completa=True).count()
        num_art_comprados = articulos.count()
    
        if num_art_comprados == num_art_entregados:
            print(f'Éxito para OC con ID {compra.id}')
            compra.entrada_completa = True
            compra.save()

            # Incrementamos el contador y agregamos la ID a la lista
            oc_modificadas += 1
            ids_modificadas.append(compra.id)

    # Informe final:
    print("Proceso completado.")
    print(f"Total de OC modificadas: {oc_modificadas}")
    print(f"IDs de OC modificadas: {ids_modificadas}")
