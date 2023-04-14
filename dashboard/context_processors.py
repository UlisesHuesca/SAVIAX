from genericpath import exists
from itertools import count
from dashboard.models import ArticulosparaSurtir, Order
from tesoreria.models import Pago
from compras.models import Compra
from requisiciones.models import Requis, ValeSalidas
from compras.models import Compra
from user.models import Profile, Tipo_perfil
from django.db.models import Q

def contadores_processor(request):
    #Por si aun no se ingresa a un perfil para que no se trabe en el login
    #usuario = Profile.objects.filter(staff__id = request.user.id)
    usuario = Profile.objects.filter(staff__id=request.user.id)

    conteo_requis = 0
    conteo_oc = 0
    conteo_pagos = 0
    conteo_solicitudes = 0
    conteo_requis_pendientes = 0
    conteo_salidas = 0
    conteo_oc1 = 0
    conteo_entradas = 0


    if not usuario:
        #Profile.objects.filter(staff__id=request.user.id):
        #productos= ArticulosparaSurtir.objects.filter(salida=False, articulos__orden__autorizar = True, articulos__producto__producto__servicio = False, articulos__orden__tipo__tipo="normal")
        #ordenes_por_autorizar = Order.objects.filter(complete=True, autorizar=None)
        conteo = 0
        conteo_ordenes = 0
        usuario = None
    else:
        #productos= ArticulosparaSurtir.objects.filter(salida=False, articulos__orden__autorizar = True, articulos__producto__producto__servicio = False, articulos__orden__tipo__tipo="normal")
        #productos= productos.filter(articulos__orden__superintendente=usuario)
        ordenes = Order.objects.filter(complete=True, autorizar = True)

        requis = Requis.objects.filter(complete = True)
        conteo = requis.count()
        usuario = usuario[0]

        if usuario.tipo.compras == True:
            requis= Requis.objects.filter(complete=True, autorizar=True, colocada=False)
            conteo_requis = requis.count()
        if usuario.tipo.oc_superintendencia == True:
            oc = Compra.objects.filter(complete=True, autorizado1=None)
            conteo_oc1 = oc.count()
        if usuario.tipo.oc_gerencia == True:
            oc = Compra.objects.filter(autorizado1= True, autorizado2=None)
            conteo_oc = oc.count()
        if usuario.tipo.tesoreria == True:
            oc_pendientes = Compra.objects.filter(pagada=False, autorizado2=True)
            conteo_pagos = oc_pendientes.count()
        if usuario.tipo.supervisor == True:
            solicitudes_pendientes = Order.objects.filter(autorizar = None, complete = True)
            conteo_solicitudes = solicitudes_pendientes.count()
        if usuario.tipo.superintendente == True:
            requisiciones_pendientes = Requis.objects.filter(complete=True, autorizar=None)
            conteo_requis_pendientes = requisiciones_pendientes.count()
        if usuario.tipo.almacen == True:
            entradas = Compra.objects.filter(pagada = True, entrada_completa = False)
            conteo_entradas = entradas.count()


    return {
    'conteo_requis_pendientes':conteo_requis_pendientes,
    'conteo_entradas':conteo_entradas,
    'conteo_solicitudes': conteo_solicitudes,
    'conteodeordenes':conteo,
    'conteo_oc': conteo_oc,
    'conteo_oc1':conteo_oc1,
    'usuario':usuario,
    'conteo_requis': conteo_requis,
    'conteo_pagos':conteo_pagos,
    }