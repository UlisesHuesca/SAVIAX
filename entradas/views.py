from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from compras.models import Compra, ArticuloComprado
from compras.filters import CompraFilter
from dashboard.models import Inventario, Order, ArticulosparaSurtir
from requisiciones.models import Salidas
from .models import Entrada, EntradaArticulo
from .forms import EntradaArticuloForm
from user.models import Profile
import json
from django.db.models import Sum
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from djmoney.money import Money

# Create your views here.
@login_required(login_url='user-login')
def pendientes_entrada(request):
    compras = Compra.objects.filter(Q(cond_de_pago = 0) | Q(pagada = True), entrada_completa = False, autorizado2= True).order_by('-folio')
    myfilter = CompraFilter(request.GET, queryset=compras)
    compras = myfilter.qs

    context = {
        'compras':compras,
        'myfilter':myfilter,
        }

    return render(request, 'entradas/pendientes_entrada.html', context)

@login_required(login_url='user-login')
def articulos_entrada(request, pk):
    usuario = Profile.objects.get(id=request.user.id)
    articulos = ArticuloComprado.objects.filter(oc=pk, entrada_completa = False)
    compra = Compra.objects.get(id=pk)
    entrada, created = Entrada.objects.get_or_create(oc=compra, almacenista= usuario, completo = False)
    articulos_entrada = EntradaArticulo.objects.filter(entrada = entrada, articulo_comprado__entrada_completa = True)
    form = EntradaArticuloForm()




    for articulo in articulos:
        if articulo.cantidad_pendiente == None:
            articulo.cantidad_pendiente = articulo.cantidad



    if request.method == 'POST' and 'entrada' in request.POST:
        num_art_comprados = articulos.count()
        entrada.completo = True
        num_art_entregados = articulos.filter(entrada_completa=True).count()
        if entrada.oc.req.orden.tipo.tipo == 'resurtimiento':
            for articulo in articulos_entrada:
                producto_surtir = ArticulosparaSurtir.objects.get(articulos__producto = articulo.articulo_comprado.producto.producto.articulos.producto, surtir=False, requisitar=True)
                producto_surtir.surtir = True
                producto_surtir.requisitar=False
                producto_surtir.save()
        #Se compara los articulos comprados contra los articulos que han entrado y que están totalmente entregados
        if num_art_comprados == num_art_entregados:
            compra.entrada_completa = True
        compra.save()
        entrada.save()
        messages.success(request, f'La entrada {entrada.id} se ha realizado con éxito')
        return redirect('pendientes_entrada')


    context = {
        'articulos':articulos,
        'entrada':entrada,
        'compra':compra,
        'form':form,
        'articulos_entrada':articulos_entrada,
        }

    return render(request, 'entradas/articulos_entradas.html', context)

def update_entrada(request):
    data = json.loads(request.body)


    action = data["action"]
    cantidad = int(data["cantidad_ingresada"])
    producto_id = int(data["producto"])
    pk = int(data["entrada_id"])
    producto_comprado = ArticuloComprado.objects.get(id = producto_id)
    entrada = Entrada.objects.get(id = pk, completo = False)
    entradas_producto = EntradaArticulo.objects.filter(articulo_comprado = producto_comprado, entrada__oc = producto_comprado.oc, entrada__completo = True).aggregate(Sum('cantidad'))
    entrada_item, created = EntradaArticulo.objects.get_or_create(entrada = entrada, articulo_comprado = producto_comprado)
    producto_inv = Inventario.objects.get(producto = producto_comprado.producto.producto.articulos.producto.producto)
    if entrada.oc.req.orden.tipo.tipo == 'resurtimiento':
        producto_surtir = ArticulosparaSurtir.objects.filter(articulos__producto = producto_comprado.producto.producto.articulos.producto, surtir=False, requisitar=True)
    else:
        producto_surtir = ArticulosparaSurtir.objects.get(articulos = producto_comprado.producto.producto.articulos)
    suma_entradas = entradas_producto['cantidad__sum']
    monto_inventario = producto_inv.cantidad * producto_inv.price + producto_inv.cantidad_apartada * producto_inv.price * producto_inv.price
    cantidad_inventario = producto_inv.cantidad + producto_inv.cantidad_apartada
    if suma_entradas is None:
        suma_entradas = 0
    if action == "add":
        total_entradas = suma_entradas + cantidad
        if suma_entradas > producto_comprado.cantidad: #Si la cantidad de las entradas es mayor a la cantidad de la compra se rechaza
            messages.error(request,f'La cantidad que se quiere comprar sobrepasa la cantidad comprada {suma_entradas} > {cantidad}')
        else:
            entrada_item.cantidad = cantidad
            entrada_item.cantidad_por_surtir = cantidad
            producto_comprado.cantidad_pendiente = producto_comprado.cantidad - total_entradas
            #Se modifica el inventario
            monto_total = monto_inventario + entrada_item.cantidad * producto_comprado.precio_unitario
            cantidad_total =  cantidad_inventario + entrada_item.cantidad
            precio_unit_promedio = monto_total/cantidad_total
            producto_inv.price = precio_unit_promedio
            if entrada.oc.req.orden.tipo.tipo == 'resurtimiento':
                if producto_surtir.exists():
                    for producto in producto_surtir:
                        producto_inv.cantidad_entradas = producto_inv.cantidad_entradas + entrada_item.cantidad
                        if producto.cantidad_requisitar > entrada_item.cantidad:                                 #Si el producto pendiente de requisitar es mayor que las entradas
                            producto.cantidad = producto.cantidad + entrada_item.cantidad                        #Al producto disponible para surtir se le suma lo que entra
                            producto.cantidad_requisitar = producto.cantidad_requisitar - entrada_item.cantidad  #Al producto pendiente por requisitar se le resta lo que entra
                            #entrada_item.cantidad_por_surtir = 0                                                 #Se agota la entrada del artículo
                            #entrada_item.agotado = True
                            producto_inv.cantidad_apartada = producto_inv.cantidad_apartada + entrada_item.cantidad
                            producto_inv.cantidad_entradas = producto_inv.cantidad_entradas + entrada_item.cantidad
                        if producto.cantidad_requisitar <= entrada_item.cantidad:                 #Si el producto pendiente de requisitar es menor o igual que las entradas
                            producto.cantidad = producto.cantidad_requisitar                      #la cantidad disponible para surtir es igual a la cantidad por requisitar, es decir, se cubre toda la necesidad
                            producto_inv.cantidad_apartada = producto_inv.cantidad_apartada + producto.cantidad_requisitar #la cantidad que se aparta es solo la cantidad que estaba pendiente por requisitar
                            producto_inv.cantidad = producto_inv.cantidad + entrada_item.cantidad - producto.cantidad_requisitar #El producto disponible en el inventario es la suma de lo que ya estaba ahí más lo que entró menos lo que ho se había surtido y que ahora queda apartado
                            producto_inv.cantidad_entradas = producto_inv.cantidad_entradas + entrada_item.cantidad  #El producto disposible proveniente de entradas en el almacén es igual al que ya estaba proveniente de las entradas mas la nueva entrada
                            producto.cantidad_requisitar = 0                                                         #Al cubrirse toda la necesidad la cantidad por requisitar pasa a 0
                            solicitud = Order.objects.get(id = producto.articulos.orden.id)
                            solicitud.requisitar = False
                        #producto_surtir.surtir = True
                        producto.save()
                        solicitud.save()
                        producto_inv.save()
                producto_inv._change_reason = 'Se modifica el inventario en view: update_entrada. Esto es una entrada para resurtimiento'
            else:
                producto_inv.cantidad_apartada = entrada_item.cantidad + producto_inv.cantidad_apartada
                producto_inv.cantidad_entradas = producto_inv.cantidad_entradas + entrada_item.cantidad
                #Se modifican la disponibilidad de los productos, es decir, quedan para surtir
                producto_surtir.cantidad = producto_surtir.cantidad + entrada_item.cantidad
                producto_inv._change_reason = 'Se modifica el inventario en view: update_entrada. Esto es una entrada para solicitud normal'
                #producto_surtir.surtir = True
            #Se guardan todas las bases de datos
            if producto_comprado.cantidad == total_entradas:  #Si la cantidad de la compra es igual a la cantida entonces la entrada está completamente entregada
                producto_comprado.entrada_completa = True
            messages.success(request,f'Estas son la cantidad de productos entregados hasta ahora: {producto_comprado.entrada_completa}')
            if producto_comprado.producto.producto.articulos.producto.producto.servicio == True:
                salida, created = Salidas.objects.get_or_create(producto = producto_surtir, salida_firmada=True, cantidad = entrada_item.cantidad)
                salida.comentario = 'Esta salida es un  servicio por lo tanto no pasa por almacén y no existe registro de la salida del mismo'
                producto_inv.cantidad_apartada = 0
                producto_surtir.surtir = False
                salida.save()
            entrada_item.save()
            producto_comprado.save()
            producto_inv.save()
            if producto_surtir and entrada.oc.req.orden.tipo.tipo == 'normal':
                producto_surtir.save()

    elif action == "remove":
        monto_total = monto_inventario - entrada_item.cantidad * producto_comprado.precio_unitario
        cantidad_total = cantidad_inventario - entrada_item.cantidad
        producto_inv.price = monto_total/cantidad_total
        if entrada.oc.req.orden.tipo.tipo == 'resurtimiento':
            for producto in producto_surtir:
                if producto.cantidad > entrada_item.cantidad:
                    producto.cantidad = producto.cantidad - entrada_item.cantidad
                if producto.cantidad <= entrada_item.cantidad:
                    producto.cantidad_requisitar = producto.cantidad
                    producto_inv.cantidad = producto_inv.cantidad - entrada_item.cantidad + producto.cantidad
                    producto.cantidad = 0
                    producto_inv.cantidad_apartada = producto_inv.cantidad_apartada - producto.cantidad_requisitar
                    solicitud = Order.objects.get(id = producto.articulos.orden.id)
                    solicitud.requisitar = False
                    #producto.surtir=False
                    #producto.requisitar = True
                    producto.save()
                    solicitud.save()
        else:
            producto_inv.cantidad_apartada = producto_inv.cantidad_apartada - entrada_item.cantidad
        producto_inv._change_reason = 'Se está borrando una entrada. view: update_entrada'
        if producto_surtir and entrada.oc.req.orden.tipo.tipo == 'normal':
            producto_surtir.cantidad = producto_surtir.cantidad - entrada_item.cantidad
            producto_surtir.surtir=False
            producto_surtir.precio = 0
            producto_surtir.save()
        #Esta es la parte que falla
        producto_comprado.cantidad_pendiente = producto_comprado.cantidad_pendiente + entrada_item.cantidad
        producto_comprado.entrada_completa = False
        messages.success(request,f'Estas son la cantidad de productos entregados hasta ahora: {producto_comprado.cantidad_pendiente}')
        #Se borra el elemento de las entradas
        #Guardado de bases de datos
        entrada_item.save()
        producto_inv.save()
        producto_comprado.save()
        entrada_item.delete()
    return JsonResponse('Item was '+action, safe=False)

