from dashboard.models import ArticulosparaSurtir

def contadores_processor(request):
    productos= ArticulosparaSurtir.objects.filter(salida=False, articulos__orden__autorizar = True, articulos__producto__producto__servicio = False)
    prod = []
    for producto in productos:
        if producto.articulos.orden not in prod:
            prod.append(producto.articulos.orden)

    conteo = len(prod)

    return {

    'conteodeordenes':conteo

    }