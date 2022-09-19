from dashboard.models import ArticulosparaSurtir, Order

def contadores_processor(request):
    productos= ArticulosparaSurtir.objects.filter(salida=False, articulos__orden__autorizar = True, articulos__producto__producto__servicio = False, articulos__orden__tipo__tipo="normal")
    ordenes_por_autorizar = Order.objects.filter(complete=True, autorizar=None)
    prod = []
    for producto in productos:
        if producto.articulos.orden not in prod:
            prod.append(producto.articulos.orden)

    conteo_pendientes = len(ordenes_por_autorizar)
    conteo = len(prod)

    return {
    'conteo_pendientes':conteo_pendientes,
    'conteodeordenes':conteo
    }