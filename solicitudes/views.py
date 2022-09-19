from django.shortcuts import render, redirect
from dashboard.models import Inventario, Order, ArticulosOrdenados, ArticulosparaSurtir
from requisiciones.models import Requis, ArticulosRequisitados
from compras.models import Compra, ArticuloComprado
from solicitudes.models import Subproyecto
from dashboard.models import Product, Tipo_Orden
from entradas.models import EntradaArticulo
from .forms import InventarioForm, OrderForm, Inv_UpdateForm, ArticulosOrdenadosForm
from user.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import json
from django.db.models import Sum
from .filters import InventoryFilter, SolicitudesFilter, SolicitudesProdFilter
from django.contrib import messages
# Import Pagination Stuff
from django.core.paginator import Paginator
from datetime import date, datetime
from djmoney.money import Money
# Import Excel Stuff
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib import messages
from django.db.models import Sum
from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Font, PatternFill
from openpyxl.utils import get_column_letter
import datetime as dt
from django.core.mail import send_mail
from django.db.models import F
# Create your views here.


#Respuesta de Json

def updateItem(request):
    data= json.loads(request.body)
    productId = data['productId']
    action = data['action']

    usuario = Profile.objects.get(id=request.user.id)
    producto = Inventario.objects.get(id=productId)
    tipo = Tipo_Orden.objects.get(tipo ='normal')
    order, created = Order.objects.get_or_create(staff=usuario, complete=False, tipo = tipo)

    orderItem, created = ArticulosOrdenados.objects.get_or_create(orden = order, producto= producto)

    if action == 'add':
        orderItem.cantidad = (orderItem.cantidad + 1)
        message = f"Item was added: {orderItem}"
        orderItem.save()
    elif action == 'remove':
        orderItem.delete()
        message = f"Item was removed: {orderItem}"

    return JsonResponse(message, safe=False)

def updateItemRes(request):
    data= json.loads(request.body)
    productId = data['productId']
    action = data['action']

    usuario = Profile.objects.get(id=request.user.id)
    producto = Inventario.objects.get(id=productId)
    tipo = Tipo_Orden.objects.get(tipo ='resurtimiento')
    order, created = Order.objects.get_or_create(staff=usuario, complete=False, tipo = tipo)
    orderItem, created = ArticulosOrdenados.objects.get_or_create(orden = order, producto= producto)

    if action == 'add':
        orderItem.cantidad = (orderItem.cantidad + 1)
        message = f"Item was added: {orderItem}"
        orderItem.save()
    elif action == 'remove':
        orderItem.delete()
        message = f"Item was removed: {orderItem}"

    return JsonResponse(message, safe=False)

#Vista de seleccion de productos, requiere login
@login_required(login_url='user-login')
def product_selection_resurtimiento(request):
    usuario = Profile.objects.get(id=request.user.id)
    tipo = Tipo_Orden.objects.get(tipo ='resurtimiento')
    order, created = Order.objects.get_or_create(staff=usuario, complete=False, tipo=tipo)
    productos = Inventario.objects.filter(cantidad__lte =F('minimo'))
    cartItems = order.get_cart_quantity
    myfilter=InventoryFilter(request.GET, queryset=productos)
    productos = myfilter.qs


    context= {
        'myfilter': myfilter,
        'productos':productos,
        'productosordenadosres':cartItems,
        }
    return render(request, 'solicitud/product_selection_resurtimiento.html', context)


#Vista de seleccion de productos, requiere login
@login_required(login_url='user-login')
def product_selection(request):
    usuario = Profile.objects.get(id=request.user.id)
    tipo = Tipo_Orden.objects.get(tipo ='normal')
    order, created = Order.objects.get_or_create(staff = usuario, complete = False, tipo = tipo)
    productos = Inventario.objects.all()
    cartItems = order.get_cart_quantity
    myfilter=InventoryFilter(request.GET, queryset=productos)
    productos = myfilter.qs


    context= {
        'myfilter': myfilter,
        'productos':productos,
        'productosordenados':cartItems,
        }
    return render(request, 'solicitud/product_selection.html', context)



#Vista del carro de compras
#@login_required(login_url='user-login')
#def cart(request):
#    staff = Profile.objects.get(id = request.user.id)

#    orden = Order.objects.filter(staff = staff, complete = False, autorizar=None, tipo__tipo="normal")
    #productos = orden.articulosordenados_set.all()
#    productos = ArticulosOrdenados.objects.filter(id__orden = orden.id)
#    cartItems = orden.get_cart_quantity

#    context= {
#        'productos':productos,
#        'orden':orden,
#        'productosordenados':cartItems,
#    }
#    return render(request, 'solicitud/cart.html', context)

#Vista para crear solicitud
@login_required(login_url='user-login')
def checkout(request):
    usuario = Profile.objects.get(id=request.user.id)
    #Tengo que revisar primero si ya existe una orden pendiente del usuario
    orders = Order.objects.filter(staff__distrito = usuario.distrito)
    consecutivo = orders.count() + 1
    tipo = Tipo_Orden.objects.get(tipo ='normal')
    order, created = Order.objects.get_or_create(staff = usuario, complete = False, tipo=tipo)

    if order.staff != usuario:
        productos = None
        cartItems = 0
    else:
        productos = order.articulosordenados_set.all()
        cartItems = order.get_cart_quantity

    form = OrderForm(instance=order, distrito = usuario.distrito)


    if request.method =='POST':
        form = OrderForm(request.POST, instance=order, distrito = usuario.distrito)
        order.complete = True
        order.created_at = date.today()
        order.created_at_time = datetime.now().time()

        abrev= usuario.distrito.abreviado
        order.folio = str(abrev) + str(consecutivo).zfill(4)
        if form.is_valid():
            order.save()
            form.save()
            messages.success(request, f'La solicitud {order.folio} ha sido creada')
            cartItems = '0'
            return redirect('solicitud-matriz')


    context= {
        'form':form,
        'productos':productos,
        'orden':order,
        'productosordenados':cartItems,
    }
    return render(request, 'solicitud/checkout.html', context)

def product_quantity_edit(request, pk):
    item = ArticulosOrdenados.objects.get(id= pk)
    form= ArticulosOrdenadosForm(instance = item)

    if request.method == 'POST':
        form = ArticulosOrdenadosForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)

    context = {
        'form': form,
        'item':item,
        }

    return render(request, 'solicitud/product_quantity_edit.html', context)

#Vista para crear solicitud
@login_required(login_url='user-login')
def checkout_resurtimiento(request):
    usuario = Profile.objects.get(id=request.user.id)
    #Tengo que revisar primero si ya existe una orden pendiente del usuario
    orders = Order.objects.filter(staff__distrito = usuario.distrito, complete = False)
    consecutivo = orders.count()+1


    tipo = Tipo_Orden.objects.get(tipo ='resurtimiento')
    order, created = Order.objects.get_or_create(staff = usuario, complete = False, tipo=tipo)

    if order.staff != usuario:
        productos = None
        cartItems = 0
    else:
        productos = order.articulosordenados_set.all()
        cartItems = order.get_cart_quantity

    form = OrderForm(instance=order, distrito = usuario.distrito)


    if request.method =='POST':
        form = OrderForm(request.POST, instance=order, distrito = usuario.distrito)
        order.complete = True
        order.created_at = date.today()
        order.created_at_time = datetime.now().time()

        abrev= usuario.distrito.abreviado
        order.folio = str(abrev) + str(consecutivo).zfill(4)
        if form.is_valid():
            order.save()
            form.save()
            messages.success(request, f'La solicitud {order.folio} ha sido creada')
            cartItems = '0'
            return redirect('solicitud-matriz')

    context= {
        'form':form,
        'productos':productos,
        'orden':order,
        'productosordenadosres':cartItems,
    }
    return render(request, 'solicitud/checkout_resurtimiento.html', context)


#Vista para crear solicitud
@login_required(login_url='user-login')
def checkout_editar(request, pk):

    order = Order.objects.get(id=pk)

    usuario = Profile.objects.get(id=request.user.id)

    productos = order.articulosordenados_set.all()
    cartItems = order.get_cart_quantity
    form = OrderForm(instance=order, distrito = usuario.distrito)


    if request.method =='POST':
        form = OrderForm(request.POST, instance=order, distrito = usuario.distrito)
        order.complete = True
        if form.is_valid():
            form.save()
            cartItems = '0'
            return redirect('solicitud-matriz')

    context= {
        'form':form,
        'productos':productos,
        'orden':order,
        'productosordenados':cartItems,
    }
    return render(request, 'solicitud/checkout.html', context)

@login_required(login_url='user-login')
def solicitud_pendiente(request):

    #El filtro de usuario, obtengo el id de usuario, busco el perfil que hace match, lo pasó como argumento
    # de filtro
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)

    #Este es un filtro por usuario general solo puede ver sus solicitudes
    productos = ArticulosOrdenados.objects.filter(orden__complete=False, orden__staff=perfil).order_by('-orden__folio')

    context= {
         'productos':productos,
        }
    return render(request, 'solicitud/solicitudes_pendientes.html',context)

@login_required(login_url='user-login')
def solicitud_matriz(request):
    #obtengo el id de usuario, lo paso como argumento a id de profiles para obtener el objeto profile que coindice con ese usuario_id
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)


    #Este es un filtro por perfil supervisor o superintendente, es decir puede ver todo lo del distrito
    ordenes = Order.objects.filter(complete=True, staff__distrito=perfil.distrito).order_by('-folio')
    myfilter=SolicitudesFilter(request.GET, queryset=ordenes)
    ordenes = myfilter.qs

    #Set up pagination
    p = Paginator(ordenes, 10)
    page = request.GET.get('page')
    ordenes_list = p.get_page(page)

    if request.method =='POST' and 'btnExcel' in request.POST:

        return convert_excel_solicitud_matriz(ordenes)

    context= {
        'ordenes_list':ordenes_list,
        'myfilter':myfilter,
        }

    return render(request, 'solicitud/solicitudes_creadas.html',context)


@login_required(login_url='user-login')
def solicitud_matriz_productos(request):

    #Aquí aparecen todoas las ordenes, es decir sería el filtro para administrador
    productos = ArticulosOrdenados.objects.filter(orden__complete=True).order_by('-orden__folio')
    myfilter=SolicitudesProdFilter(request.GET, queryset=productos)
    productos = myfilter.qs

    #Set up pagination
    p = Paginator(productos, 15)
    page = request.GET.get('page')
    productos_list = p.get_page(page)

    if request.method =='POST' and 'btnExcel' in request.POST:

        return convert_excel_solicitud_matriz_productos(productos)

    context= {
        'productos':productos_list,
        'myfilter':myfilter,
        }
    return render(request, 'solicitud/solicitudes_creadas_productos.html',context)



@login_required(login_url='user-login')
def inventario(request):
    existencia = Inventario.objects.filter(complete=True, producto__servicio = False).order_by('producto__codigo')
    entries = EntradaArticulo.objects.all()
    entradas = entries.annotate(Sum('cantidad'))
    for item in existencia:
        query = entries.filter(articulo_comprado__producto__producto__articulos__producto = item, agotado = False)
        if query.exists():
            cantidad = query.aggregate(Sum('cantidad_por_surtir'))
            item.cantidad_entradas = cantidad['cantidad_por_surtir__sum']
            item.save()


    #apartado = ArticulosparaSurtir.objects.values('articulos__producto__producto__codigo').annotate(cantidad_total=Sum('cantidad'))
    #Este es el metodo que utilicé para multiplicar 2 columnas de un mismo modelo y devolver el total
    list_inv = existencia.values_list('cantidad', 'cantidad_apartada','price')
    valor_inv_raw = sum((t[0] + t[1])*t[2] for t in list_inv)
    valor_inv = Money(valor_inv_raw,'MXN')

    if request.method =='POST' and 'btnExcel' in request.POST:
        return convert_excel_inventario(existencia, valor_inv_raw )

    context = {
        'existencia' : existencia,
        'entradas':entradas,
        'valor_inv': valor_inv,
        }

    return render(request,'dashboard/inventario.html', context)

def inventario_add(request):
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)
    productos = Inventario.objects.filter(complete = False, producto__completado = True)
    form = InventarioForm()

    if request.method =='POST':
        form = InventarioForm(request.POST)
        item = form.save(commit=False)
        item.complete = True
        item._change_reason = 'Se agrega producto el inventario en view: inventario_add'
        item.distrito = perfil.distrito
        if form.is_valid():
            form.save()
            item.save()
            return HttpResponse(status=204)
    #else:
        #form = InventarioForm()



    context = {
        'form': form,
        'productos':productos,
        }

    return render(request,'dashboard/inventario_add.html',context)

@login_required(login_url='user-login')
def inventario_update_modal(request, pk):
    #usuario = request.user.id
    #perfil = Profile.objects.get(id=usuario)
    item = Inventario.objects.get(id=pk)


    if request.method =='POST':
        form = Inv_UpdateForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item._change_reason = item.comentario +'. Se modifica inventario en view: inventario_update_modal'
            item.save()
            messages.success(request, f'El artículo {item.producto.codigo}:{item.producto.nombre} se ha actualizado exitosamente')
            return HttpResponse(status=204)
    else:
        form = Inv_UpdateForm(instance=item)

    context = {
        'form': form,
        'item':item,
        }
    #return render(request,'dashboard/inventario_update.html', context)
    return render(request,'dashboard/inventario_update_modal.html',context)


@login_required(login_url='user-login')
def historico_inventario(request):
    registros = Inventario.history.all()

    context = {
        'registros':registros,
        }

    return render(request,'dashboard/historico_inventario.html',context)


@login_required(login_url='user-login')
def inventario_delete(request, pk):
    item = Inventario.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('solicitud-inventario')

    return render(request,'dashboard/inventario_delete.html')

@login_required(login_url='user-login')
def solicitud_autorizacion(request):
    #obtengo el id de usuario, lo paso como argumento a id de profiles para obtener el objeto profile que coindice con ese usuario_id
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)

    #Este es un filtro por perfil supervisor o superintendente, es decir puede ver todo lo del distrito
    ordenes = Order.objects.filter(complete=True, autorizar=None, staff__distrito=perfil.distrito).order_by('-folio')
    myfilter=SolicitudesFilter(request.GET, queryset=ordenes)
    ordenes = myfilter.qs


    context= {
        'myfilter':myfilter,
        'ordenes':ordenes,
        }

    return render(request, 'autorizacion/solicitudes_pendientes_autorizacion.html',context)

def detalle_autorizar(request, pk):
    productos = ArticulosOrdenados.objects.filter(orden=pk)

    context = {
        'productos': productos,
     }
    return render(request,'autorizacion/detail.html', context)

@login_required(login_url='user-login')
def autorizada_sol(request, pk):
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)
    order = Order.objects.get(id = pk)
    productos = ArticulosOrdenados.objects.filter(orden = pk)
    requis = Requis.objects.filter(orden__staff__distrito = perfil.distrito)
    consecutivo = requis.count() + 1

    if request.method =='POST':
        #We go trough all the products one by one contained in the order
        for producto in productos:
            # We fetch inventory product corresponding to product (that's why we use product.id)
            # We create a new product line in a new database to control the ArticlestoDeliver (ArticulosparaSurtir)
            prod_inventario = Inventario.objects.get(id = producto.producto.id)
            #if prod_inventario.cantidad_entradas > 0:
                #entradas = EntradaArticulo.objects.filter(articulo_comprado__producto__producto__articulos = producto, agotado = False).order_by('id')
            ordensurtir , created = ArticulosparaSurtir.objects.get_or_create(articulos = producto)
            #cond:1 evalua si la cantidad en inventario es mayor que lo solicitado
            if prod_inventario.cantidad >= producto.cantidad and order.tipo.tipo == "normal":
                prod_inventario.cantidad = prod_inventario.cantidad - producto.cantidad
                prod_inventario.cantidad_apartada = producto.cantidad + prod_inventario.cantidad_apartada
                prod_inventario._change_reason = f'Se modifica el inventario en view: autorizada_sol:{order.id} cond:1'
                ordensurtir.cantidad = producto.cantidad
                ordensurtir.precio = prod_inventario.price
                ordensurtir.surtir = True
                ordensurtir.requisitar = False
                ordensurtir.save()
                prod_inventario.save()
            elif producto.cantidad >= prod_inventario.cantidad and prod_inventario.cantidad > 0 and order.tipo.tipo == "normal": #si la cantidad solicitada es mayor que la cantidad en inventario
                ordensurtir.cantidad = prod_inventario.cantidad #lo que puedes surtir es igual a lo que tienes en el inventario
                ordensurtir.precio = prod_inventario.price
                #total = ordensurtir.cantidad * ordensurtir.precio
                ordensurtir.cantidad_requisitar = producto.cantidad - ordensurtir.cantidad #lo que falta por surtir
                prod_inventario.cantidad_apartada = prod_inventario.cantidad_apartada + prod_inventario.cantidad
                prod_inventario.cantidad = 0
                ordensurtir.surtir = True
                ordensurtir.requisitar=True
                prod_inventario.save()
                ordensurtir.save()
                #if ordensurtir.cantidad_requisitar > 0: #si lo que falta por surtir es mayor que 0
                #    for entrada in entradas:
                #        if entrada.cantidad_por_surtir > ordensurtir.cantidad_requisitar and ordensurtir.cantidad_requisitar > 0:
                #            entrada.cantidad = entrada.cantidad_por_surtir - ordensurtir.cantidad_requisitar
                #            total = total + ordensurtir.cantidad_requisitar * entrada.articulo_comprado.precio_unitario
                #            ordensurtir.cantidad = ordensurtir.cantidad + entrada.cantidad_por_surtir
                #            ordensurtir.precio = total/ordensurtir.cantidad
                #            ordensurtir.cantidad_requisitar = 0  #Aquí ya no habría nada que requisitar
                #            ordensurtir.surtir = True

                #        elif entrada.cantidad_por_surtir <= ordensurtir.cantidad_requisitar and ordensurtir.cantidad_requisitar > 0:
                #            ordensurtir.cantidad_requisitar = ordensurtir.cantidad_requisitar - entrada.cantidad_por_surtir
                #            entrada.cantidad_cantidad_por_surtir = 0 # En este escenario se agota una las entradas
                #            total = total + entrada.cantidad_por_surtir * entrada.articulo_comprado.precio_unitario
                #            ordensurtir.cantidad = ordensurtir.cantidad + entrada.cantidad_por_surtir
                #            ordensurtir.precio = total/ordensurtir.cantidad
                #            entrada.agotado = True
                #        entrada.save()

                #    ordensurtir.save()
                #    if ordensurtir.cantidad_requisitar > 0:
                #        ordensurtir.requisitar=True
                #        order.requisitar=True
                #    order.save()
                #elif ordensurtir.cantidad_requisitar > 0 and prod_inventario.cantidad_entradas < 0:
                #    ordensurtir.requisitar = True
                #    order.requisitar = True
                #    ordensurtir.save()
                #    order.save()
            #cond:3
            elif prod_inventario.cantidad + prod_inventario.cantidad_entradas == 0 or order.tipo.tipo == "resurtimiento":
                ordensurtir.requisitar = True
                ordensurtir.cantidad_requisitar = producto.cantidad
                order.requisitar = True
                if producto.producto.producto.servicio == True:
                    requi, created = Requis.objects.get_or_create(complete = True, orden = order)
                    requitem, created = ArticulosRequisitados.objects.create(req = requi, producto= ordensurtir, cantidad = producto.cantidad)
                    requi.folio = str(usuario.distrito.abreviado)+str(consecutivo).zfill(4)
                    order.requisitar=False
                    ordensurtir.requisitar=False
                    requi.save()
                    requitem.save()
                ordensurtir.save()
                order.save()
        order.autorizar = True
        order.approved_at = date.today()
        order.approved_at_time = datetime.now().time()
        send_mail(
            f'Solicitud Autorizada {order.folio}',
            f'{order.staff.staff.first_name}, la solicitud {order.folio} ha sido autorizada. Este mensaje ha sido automáticamente generado por SAVIA X',
            'saviax.vordcab@gmail.com',
            [order.staff.staff.email],
            )
        order.sol_autorizada_por = Profile.objects.get(id=request.user.id)
        order.save()

        messages.success(request, f'{perfil.staff.first_name} has autorizado la solicitud {order.folio}')
        return redirect('solicitud-pendientes-autorizacion')


    context = {
        'orden': order,
        'productos': productos,
    }

    return render(request,'autorizacion/autorizada.html', context)

def cancelada_sol(request, pk):
    order = Order.objects.get(id = pk)
    productos = ArticulosOrdenados.objects.filter(orden = pk)

    if request.method =='POST':
        order.autorizar = False
        order.save()
        messages.error(request, f'La orden {order} ha sido cancelada')
        return redirect('solicitud-pendientes-autorizacion')


    context = {
        'orden': order,
        'productos': productos,
    }

    return render(request,'autorizacion/cancelada.html', context)


def status_sol(request, pk):
    solicitud = Order.objects.get(id = pk)
    product_solicitudes = ArticulosOrdenados.objects.filter(orden=pk)
    num_prod_sol= product_solicitudes.count

    try:
        requi = Requis.objects.get(orden = pk)
    except Requis.DoesNotExist:
        requi = None



    if requi != None:
        exist_req = True
        oc = Compra.objects.filter(req=requi)
        product_requis = ArticulosRequisitados.objects.filter(req=requi)
        if oc != None:
            exist_oc=True
            context = {
            'solicitud': solicitud,
            'product_solicitudes': product_solicitudes,
            'num_prod_sol': num_prod_sol,
            'product_requis':product_requis,
            'requi': requi,
            'exist_oc': exist_oc,
            'oc':oc,
        }
        else:
            context = {
            'solicitud': solicitud,
            'product_solicitudes': product_solicitudes,
            'num_prod_sol': num_prod_sol,
            'requi': requi,
            'exist_req': exist_req,
            'oc':oc,
        }
    else:
        exist_req = False
        context = {
            'solicitud': solicitud,
            'product_solicitudes': product_solicitudes,
            'num_prod_sol': num_prod_sol,
            'exist_req': exist_req,
        }



    return render(request,'solicitud/detalle.html', context)


# AJAX
def load_subproyectos(request):

    proyecto_id = request.GET.get('proyecto_id')
    subproyectos = Subproyecto.objects.filter(proyecto_id = proyecto_id)

    return render(request, 'solicitud/subproyecto_dropdown_list_options.html',{'subproyectos': subproyectos})

def convert_excel_inventario(existencia, valor_inventario):
    response= HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename = Solicitudes_' + str(dt.date.today())+'.xlsx'
    wb = Workbook()
    ws = wb.create_sheet(title='Solicitudes')
    #Comenzar en la fila 1
    row_num = 1

    #Create heading style and adding to workbook | Crear el estilo del encabezado y agregarlo al Workbook
    head_style = NamedStyle(name = "head_style")
    head_style.font = Font(name = 'Arial', color = '00FFFFFF', bold = True, size = 11)
    head_style.fill = PatternFill("solid", fgColor = '00003366')
    wb.add_named_style(head_style)
    #Create body style and adding to workbook
    body_style = NamedStyle(name = "body_style")
    body_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(body_style)
    #Create messages style and adding to workbook
    messages_style = NamedStyle(name = "mensajes_style")
    messages_style.font = Font(name="Arial Narrow", size = 11)
    wb.add_named_style(messages_style)
    #Create date style and adding to workbook
    date_style = NamedStyle(name='date_style', number_format='DD/MM/YYYY')
    date_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(date_style)
    money_style = NamedStyle(name='money_style', number_format='$ #,##0.00')
    money_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(money_style)
    money_resumen_style = NamedStyle(name='money_resumen_style', number_format='$ #,##0.00')
    money_resumen_style.font = Font(name ='Calibri', size = 14, bold = True)
    wb.add_named_style(money_resumen_style)

    columns = ['Código','Producto','Distrito','Cantidad','Cantidad Apartada','Precio']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        if col_num == 0:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 10
        if col_num== 1:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 30
        else:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 15


    columna_max = len(columns)+2

    (ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por Savia X. UH}')).style = messages_style
    (ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Vordcab S.A. de C.V.}')).style = messages_style
    (ws.cell(column = columna_max, row = 3, value='Inventario Costo Total:')).style = messages_style
    (ws.cell(column = columna_max +1, row=3, value = valor_inventario)).style = money_resumen_style
    ws.column_dimensions[get_column_letter(columna_max)].width = 20
    ws.column_dimensions[get_column_letter(columna_max + 1)].width = 20

    rows = existencia.values_list('producto__codigo','producto__nombre','distrito__nombre','cantidad','cantidad_apartada','price')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num > 2:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = body_style
            if col_num == 5:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = money_style
            if col_num <= 2:
                (ws.cell(row = row_num, column = col_num+1, value=str(row[col_num]))).style = body_style

    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)

def convert_excel_solicitud_matriz_productos(productos):
    response= HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename = Solicitudes_por_producto_' + str(dt.date.today())+'.xlsx'
    wb = Workbook()
    ws = wb.create_sheet(title='Solicitudes')
    #Comenzar en la fila 1
    row_num = 1

    #Create heading style and adding to workbook | Crear el estilo del encabezado y agregarlo al Workbook
    head_style = NamedStyle(name = "head_style")
    head_style.font = Font(name = 'Arial', color = '00FFFFFF', bold = True, size = 11)
    head_style.fill = PatternFill("solid", fgColor = '00003366')
    wb.add_named_style(head_style)
    #Create body style and adding to workbook
    body_style = NamedStyle(name = "body_style")
    body_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(body_style)
    #Create messages style and adding to workbook
    messages_style = NamedStyle(name = "mensajes_style")
    messages_style.font = Font(name="Arial Narrow", size = 11)
    wb.add_named_style(messages_style)
    #Create date style and adding to workbook
    date_style = NamedStyle(name='date_style', number_format='DD/MM/YYYY')
    date_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(date_style)
    money_style = NamedStyle(name='money_style', number_format='$ #,##0.00')
    money_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(money_style)
    money_resumen_style = NamedStyle(name='money_resumen_style', number_format='$ #,##0.00')
    money_resumen_style.font = Font(name ='Calibri', size = 14, bold = True)
    wb.add_named_style(money_resumen_style)

    columns = ['Folio','Solicitante','Proyecto','Subproyecto','Operación','Cantidad','Código', 'Producto','Creado']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        ws.column_dimensions[get_column_letter(col_num + 1)].width = 16
        if col_num == 4 or col_num == 7:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 25



    columna_max = len(columns)+2

    (ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por Savia X. UH}')).style = messages_style
    (ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Vordcab S.A. de C.V.}')).style = messages_style
    ws.column_dimensions[get_column_letter(columna_max)].width = 20

    rows = productos.values_list('orden__id',Concat('orden__staff__staff__first_name',Value(' '),'orden__staff__staff__last_name'),'orden__proyecto__nombre','orden__subproyecto__nombre',
                                'orden__operacion__nombre','cantidad','producto__producto__codigo','producto__producto__nombre','orden__created_at')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            (ws.cell(row = row_num, column = col_num+1, value=str(row[col_num]))).style = body_style
            if col_num == 5:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = body_style
            if col_num == 8:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = date_style
    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)

def convert_excel_solicitud_matriz(ordenes):
    response= HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename = Solicitudes_' + str(dt.date.today())+'.xlsx'
    wb = Workbook()
    ws = wb.create_sheet(title='Solicitudes')
    #Comenzar en la fila 1
    row_num = 1

    #Create heading style and adding to workbook | Crear el estilo del encabezado y agregarlo al Workbook
    head_style = NamedStyle(name = "head_style")
    head_style.font = Font(name = 'Arial', color = '00FFFFFF', bold = True, size = 11)
    head_style.fill = PatternFill("solid", fgColor = '00003366')
    wb.add_named_style(head_style)
    #Create body style and adding to workbook
    body_style = NamedStyle(name = "body_style")
    body_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(body_style)
    #Create messages style and adding to workbook
    messages_style = NamedStyle(name = "mensajes_style")
    messages_style.font = Font(name="Arial Narrow", size = 11)
    wb.add_named_style(messages_style)
    #Create date style and adding to workbook
    date_style = NamedStyle(name='date_style', number_format='DD/MM/YYYY')
    date_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(date_style)
    money_style = NamedStyle(name='money_style', number_format='$ #,##0.00')
    money_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(money_style)
    money_resumen_style = NamedStyle(name='money_resumen_style', number_format='$ #,##0.00')
    money_resumen_style.font = Font(name ='Calibri', size = 14, bold = True)
    wb.add_named_style(money_resumen_style)

    columns = ['Folio','Solicitante','Proyecto','Subproyecto','Operación','Creado']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        ws.column_dimensions[get_column_letter(col_num + 1)].width = 16
        if col_num == 5:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 25

    columna_max = len(columns)+2

    (ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por Savia X. UH}')).style = messages_style
    (ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Vordcab S.A. de C.V.}')).style = messages_style
    ws.column_dimensions[get_column_letter(columna_max)].width = 20

    rows = ordenes.values_list('id',Concat('staff__staff__first_name',Value(' '),'staff__staff__last_name'),'proyecto__nombre','subproyecto__nombre',
                                'operacion__nombre','created_at')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            (ws.cell(row = row_num, column = col_num+1, value=str(row[col_num]))).style = body_style
            if col_num == 5:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = date_style
    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)