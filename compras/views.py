from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import Inventario, Order, ArticulosOrdenados, ArticulosparaSurtir, Producto_Calidad
from requisiciones.models import Requis, ArticulosRequisitados
from user.models import Profile
from tesoreria.models import Pago
from requisiciones.views import get_image_base64
from .filters import CompraFilter, ArticulosRequisitadosFilter,  ArticuloCompradoFilter, HistoricalArticuloCompradoFilter
from .models import ArticuloComprado, Compra, Proveedor, Proveedor_direcciones, Cond_credito, Uso_cfdi, Moneda, Comparativo, Item_Comparativo, Preevaluacion
from tesoreria.models import Facturas
from .forms import CompraForm, ArticuloCompradoForm, ArticulosRequisitadosForm, ComparativoForm, Item_ComparativoForm, Compra_ComentarioForm, PreevaluacionForm
from requisiciones.forms import Articulo_Cancelado_Form
from tesoreria.forms import Facturas_Form
from entradas.models import Entrada, No_Conformidad
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import json
from django.contrib import messages
from datetime import date, datetime, timedelta
from num2words import num2words
from django.core.paginator import Paginator
import decimal
from django.db.models import F, Avg, Value, ExpressionWrapper, fields, Sum, Q, Case, When, DecimalField
from django.db.models.functions import Concat, Coalesce
from django.conf import settings
#PDF generator
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import Color, black, blue, red, white
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.rl_config import defaultPageSize
from django.http import FileResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
import urllib.request, urllib.parse, urllib.error
from io import BytesIO
from django.core.mail import EmailMessage, BadHeaderError
from smtplib import SMTPException
# Import Excel Stuff
from django.contrib import messages
from openpyxl import Workbook #,save_virtual_workbook
from openpyxl.styles import NamedStyle, Font, PatternFill
from openpyxl.utils import get_column_letter
#from openpyxl.writer.excel import save_virtual_workbook
#from openpyxl import
import datetime as dt
#from urllib.parse import (
#    ParseResult,
#    SplitResult,
#    _coerce_args,
#    _splitnetloc,
#    _splitparams,
#    scheme_chars,
#)
#from urllib.parse import urlencode as original_urlencode
#from urllib.parse import uses_params
import ssl
# Create your views here.

@login_required(login_url='user-login')
def requisiciones_autorizadas(request):
    perfil = Profile.objects.get(staff__id=request.user.id)
    if perfil.tipo.compras == True:
        requis = Requis.objects.filter(autorizar=True, colocada=False)
    else:
        requis = Requis.objects.filter(complete=None)
    #requis = Requis.objects.filter(autorizar=True, colocada=False)

    tag = dof()

    context= {
        'requis':requis,
        'tags':tag,
        }

    return render(request, 'compras/requisiciones_autorizadas.html',context)

@login_required(login_url='user-login')
def productos_pendientes(request):
    perfil = Profile.objects.get(staff__id=request.user.id)
    
    if perfil.tipo.compras == True:
        requis = Requis.objects.filter(autorizar=True, colocada=False)
    else:
        requis = Requis.objects.filter(complete=None)

    articulos = ArticulosRequisitados.objects.filter(req__autorizar = True, req__colocada=False, cantidad_comprada__lt = F("cantidad"), cancelado = False)
    myfilter = ArticulosRequisitadosFilter(request.GET, queryset=articulos)
    articulos = myfilter.qs

    if request.method == 'POST' and 'btnReporte' in request.POST:
        convert_excel_productos_requisitados(articulos)
    #else:
        #messages.error(request,'Nada')


    context= {
        'requis':requis,
        'articulos':articulos,
        'myfilter':myfilter,
        #'productos_calidad': productos_calidad,
        }

    return render(request, 'compras/productos_pendientes.html',context)

def eliminar_articulos(request, pk):
    perfil = Profile.objects.get(staff__id=request.user.id)
    productos = ArticulosRequisitados.objects.filter(req = pk, cantidad_comprada__lt = F("cantidad"), cancelado=False)
    requis = Requis.objects.get(id = pk)

    form = Articulo_Cancelado_Form()

    if request.method == 'POST' and "btn_eliminar" in request.POST:
        pk = request.POST.get('id')
        producto = ArticulosRequisitados.objects.get(id=pk)
        form = Articulo_Cancelado_Form(request.POST,instance=producto)
        if form.is_valid():
            articulo = form.save()
            productos = ArticulosRequisitados.objects.filter(req = producto.req)
            productos_cancelados = productos.filter(cancelado = True).count()
            productos_requisitados = productos.count() - productos_cancelados
            productos_comprados = productos.filter(cantidad_comprada__gte = F("cantidad")).count()
            if productos_requisitados == productos_comprados:
                requis.colocada = True
                requis.save()
            email = EmailMessage(
                f'Producto Eliminado {producto.producto.articulos.producto.producto.nombre}',
                f'Estimado(a) {producto.req.orden.staff.staff.first_name}:\n\nEstás recibiendo este correo porque el producto: {producto.producto.articulos.producto.producto.nombre} de la solicitud: {producto.req.orden.folio} ha sido eliminado, por la siguiente razón: {producto.comentario_cancelacion} \n\n Atte.{perfil.staff.first_name}{perfil.staff.last_name}  \nVORDTEC DE MÉXICO S.A. de C.V.\n\n Este mensaje ha sido automáticamente generado por SAVIA VORDTEC',
                'savia@vordtec.com',
                ['ulises_huesc@hotmail.com',producto.req.orden.staff.staff.email,],
                )
            email.send()
            messages.success(request,f' Has eliminado el {producto.producto.articulos.producto} correctamente')
            return redirect('requisicion-autorizada')




    context = {
        'form':form,
        'productos': productos,
        'requis': requis,
        }

    return render(request,'compras/eliminar_articulos.html', context)

def articulos_restantes(request, pk):
    productos = ArticulosRequisitados.objects.filter(req = pk, cantidad_comprada__lt = F("cantidad"), cancelado=False)
    #productos = ArticulosRequisitados.objects.filter(req = pk, cantidad_comprada__lt = F("cantidad"))
    requis = Requis.objects.get(id = pk)

    context = {
        'productos': productos,
        'requis': requis,
        }

    return render(request,'compras/articulos_restantes.html', context)

def dof():
#Trying to fetch DOF
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = 'https://www.dof.gob.mx/#gsc.tab=0'
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html,'html.parser')
        #tags = soup.find_all('p')

        tags = []
        for tag in soup.find_all('p'):
        #for anchor in tag.find_all('span'):
            tags.append(tag.contents)

        #substr = 'DOLAR'
        #if any(substr in str for str in tags):
        #   tag = tags[str][1]


        tag = tags[4][3]

        return tag
    except Exception as e:
        # Manejo de la excepción - log, mensaje de error, etc.
        return f"Error al obtener datos: {e}"

def oc(request, pk):
    productos = ArticulosRequisitados.objects.filter(req = pk)
    req = Requis.objects.get(id = pk)
    usuario = Profile.objects.get(id=request.user.id)
    oc, created = Compra.objects.get_or_create(complete = False, req = req, creada_por = usuario)
    form_product = ArticuloCompradoForm()
    form = CompraForm(instance=oc)



    context= {
        'req':req,
        'form':form,
        'oc':oc,
        'productos':productos,
        'form_product':form_product,
        }

    return render(request, 'compras/oc.html',context)

def compras_devueltas(request):
    #productos = ArticulosRequisitados.objects.filter(req = pk)
    #req = Requis.objects.get(id = pk)
    usuario = Profile.objects.get(staff__id=request.user.id)
    compras = Compra.objects.filter(regresar_oc = True)
    myfilter = CompraFilter(request.GET, queryset=compras)
    compras = myfilter.qs

    #form_product = ArticuloCompradoForm()
    #form = CompraForm(instance=oc)



    context= {
        'myfilter':myfilter,
        'compras_list':compras,
        }

    return render(request, 'compras/compras_devueltas.html',context)

def compra_edicion(request, pk):
    usuario = Profile.objects.get(staff__id=request.user.id)
    oc = Compra.objects.get(id =pk)
    colaborador_sel = Profile.objects.all()
    productos_comp = ArticuloComprado.objects.filter(oc = oc)
    productos = ArticulosRequisitados.objects.filter(req = oc.req, sel_comp = False)
    req = Requis.objects.get(id = oc.req.id)
    proveedores = Proveedor_direcciones.objects.filter(
        Q(estatus__nombre='NUEVO') | Q(estatus__nombre='APROBADO'))
    form_product = ArticuloCompradoForm()
    form = CompraForm(instance=oc)

    tag = dof()
    subtotal = 0
    iva = 0
    total = 0
    dif_cant = 0
    form.fields['deposito_comprador'].queryset = colaborador_sel
    for item in productos_comp:
        subtotal = decimal.Decimal(subtotal + item.cantidad * item.precio_unitario)
        if item.producto.producto.articulos.producto.producto.iva == True:
            iva = round(subtotal * decimal.Decimal(0.16),2)
        total = decimal.Decimal(subtotal + decimal.Decimal(iva))

    if request.method == 'POST' and  "crear" in request.POST:
        form = CompraForm(request.POST, instance=oc)
        costo_oc = 0
        costo_iva = 0
        articulos = ArticuloComprado.objects.filter(oc=oc)
        requisitados = ArticulosRequisitados.objects.filter(req = oc.req)
        cuenta_art_comprados = requisitados.filter(art_surtido = True).count()
        cuenta_art_totales = requisitados.count()
        if cuenta_art_totales == cuenta_art_comprados and cuenta_art_comprados > 0:
            req.colocada = True
        else:
            req.colocada = False
        for articulo in articulos:
            costo_oc = costo_oc + articulo.precio_unitario * articulo.cantidad
            if articulo.producto.producto.articulos.producto.producto.iva == True:
                costo_iva = decimal.Decimal(costo_oc * decimal.Decimal(0.16))
        for producto in requisitados:
            dif_cant = dif_cant + producto.cantidad - producto.cantidad_comprada
            if producto.art_surtido == False:
                producto.sel_comp = False
                producto.save()
        oc.complete = True
        if oc.tipo_de_cambio != None and oc.tipo_de_cambio > 0:
            oc.costo_iva = decimal.Decimal(costo_iva)
            oc.costo_oc = decimal.Decimal(costo_oc + costo_iva)
        else:
            oc.costo_iva = decimal.Decimal(costo_iva)
            oc.costo_oc = decimal.Decimal(costo_oc + costo_iva)
        if form.is_valid():
            abrev= usuario.distrito.abreviado
            #oc.folio = str(abrev) + str(consecutivo).zfill(4)
            oc.regresar_oc = False
            form.save()
            oc.save()
            req.save()
            messages.success(request,f'{usuario.staff.first_name}, Has modificado la OC {oc.get_folio} correctamente')
            return redirect('compras-devueltas')



    context= {
        'proveedores':proveedores,
        'productos':productos,
        'form':form,
        'oc':oc,
        'productos_comp':productos_comp,
        'form_product':form_product,
        'subtotal':subtotal,
        'iva':iva,
        'total':total,
        }

    return render(request, 'compras/compra_edicion.html',context)



def update_oc(request):
    data= json.loads(request.body)
    action = data["action"]
    cantidad = data["val_cantidad"]
    producto_id = data["id"]
    productos = ArticulosRequisitados.objects.get(id=producto_id)
    pk = data["oc"]
    precio = data["val_precio"]
    oc = Compra.objects.get(id=pk)
    if action == "add":
        cantidad_total = productos.cantidad_comprada + decimal.Decimal(cantidad)
        if cantidad_total > productos.cantidad:
            messages.error(request,f'La cantidad que se quiere comprar sobrepasa la cantidad requisitada {cantidad_total} mayor que {productos.cantidad}')
        else:
            comp_item, created = ArticuloComprado.objects.get_or_create(oc=oc, producto=productos)
            productos.cantidad_comprada = productos.cantidad_comprada + decimal.Decimal(cantidad)
            messages.success(request,f'Estos son los productos comprados ahora {productos.cantidad_comprada}')
            if productos.cantidad_comprada == productos.cantidad:
                productos.art_surtido = True
            if comp_item.cantidad == None:
                comp_item.cantidad = 0
            comp_item.cantidad = comp_item.cantidad + decimal.Decimal(cantidad)
            comp_item.precio_unitario = precio
            productos.sel_comp = True
            comp_item.save()
            productos.save()
    if action == "remove":
        comp_item = ArticuloComprado.objects.get(oc = oc, producto = productos)
        productos.art_surtido = False
        productos.sel_comp = False
        productos.cantidad_comprada = productos.cantidad_comprada - comp_item.cantidad
        productos.save()
        comp_item.delete()

    return JsonResponse('Item updated, action executed: '+ action, safe=False)

def oc_modal(request, pk):
    #productos = ArticulosRequisitados.objects.filter(req = pk, sel_comp = False)
    productos = ArticulosRequisitados.objects.filter(req = pk, cantidad_comprada__lt = F("cantidad"), cancelado=False)
    req = Requis.objects.get(id = pk)
    proveedores = Proveedor_direcciones.objects.filter(
        Q(estatus__nombre='NUEVO') | Q(estatus__nombre='APROBADO')| Q(estatus__nombre='PREAPROBADO'))
    usuario = Profile.objects.get(staff__id=request.user.id)
    colaborador_sel = Profile.objects.all()
    compras = Compra.objects.all()
    oc, created = Compra.objects.get_or_create(complete = False, req = req, creada_por = usuario, regresar_oc = False)
    #consecutivo = compras.count() + 1
    productos_comp = ArticuloComprado.objects.filter(oc=oc)
    form_product = ArticuloCompradoForm()
    form = CompraForm(instance=oc)
    tag = dof()
    subtotal = 0
    iva = 0
    total = 0
    dif_cant = 0
    form.fields['deposito_comprador'].queryset = colaborador_sel
    for item in productos_comp:
        subtotal = decimal.Decimal(subtotal + item.cantidad * item.precio_unitario)
        if item.producto.producto.articulos.producto.producto.iva == True:
            iva = round(subtotal * decimal.Decimal(0.16),2)
        total = decimal.Decimal(subtotal + decimal.Decimal(iva))

    if request.method == 'POST' and  "crear" in request.POST:
        form = CompraForm(request.POST, instance=oc)
        
        if form.is_valid():
            costo_oc = 0
            costo_iva = 0
            articulos = ArticuloComprado.objects.filter(oc=oc)
            requisitados = ArticulosRequisitados.objects.filter(req = oc.req)
            cuenta_art_comprados = requisitados.filter(art_surtido = True).count()
            cuenta_art_totales = requisitados.count()
            if cuenta_art_totales == cuenta_art_comprados and cuenta_art_comprados > 0: #Compara los artículos comprados vs artículos requisitados
                req.colocada = True
            else:
                req.colocada = False
            for articulo in articulos:
                costo_oc = costo_oc + articulo.precio_unitario * articulo.cantidad
                if articulo.producto.producto.articulos.producto.producto.iva == True:
                    costo_iva = decimal.Decimal(costo_oc * decimal.Decimal(0.16))
            for producto in requisitados:
                dif_cant = dif_cant + producto.cantidad - producto.cantidad_comprada
                if producto.art_surtido == False:
                    producto.sel_comp = False
                    producto.save()
            oc.complete = True
            if oc.tipo_de_cambio != None and oc.tipo_de_cambio > 0:
                oc.costo_iva = decimal.Decimal(costo_iva)
                oc.costo_oc = decimal.Decimal(costo_oc + costo_iva)
            else:
                oc.costo_iva = decimal.Decimal(costo_iva)
                oc.costo_oc = decimal.Decimal(costo_oc + costo_iva)
            abrev= usuario.distrito.abreviado
            #oc.folio = str(abrev) + str(consecutivo).zfill(4)
            form.save()
            oc.save()
            req.save()
            static_path = settings.STATIC_ROOT
            img_path = os.path.join(static_path,'images','SAVIA_Logo.png')
            img_path2 = os.path.join(static_path,'images','logo vordtec_documento.png')
            image_base64 = get_image_base64(img_path)
            logo_v_base64 = get_image_base64(img_path2)
            # Crear el mensaje HTML
            html_message = f"""
            <html>
                <head>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <p><img src="data:image/jpeg;base64,{logo_v_base64}" alt="Imagen" style="width:100px;height:auto;"/></p>
                    <p>Estimado {oc.req.orden.staff.staff.first_name} {oc.req.orden.staff.staff.last_name},</p>
                    <p>Estás recibiendo este correo porque tu solicitud: {oc.req.orden.folio}| Req: {oc.req.folio} se ha convertido en la OC: {oc.get_folio},</p>
                    <p>creada por {oc.creada_por.staff.first_name} {oc.creada_por.staff.last_name}.</p>
                    <p>El siguiente paso del sistema: Autorización de OC por Superintedencia Administrativa</p>
                    <p><img src="data:image/png;base64,{image_base64}" alt="Imagen" style="width:50px;height:auto;border-radius:50%"/></p>
                    <p>Este mensaje ha sido automáticamente generado por SAVIA 2.0</p>
                </body>
            </html>
            """
            try:
                email = EmailMessage(
                    f'OC Elaborada {oc.get_folio}',
                    body=html_message,
                    #f'Estimado {requi.orden.staff.staff.staff.first_name} {requi.orden.staff.staff.staff.last_name},\n Estás recibiendo este correo porque tu solicitud: {requi.orden.folio}| Req: {requi.folio} ha sido autorizada,\n por {requi.requi_autorizada_por.staff.staff.first_name} {requi.requi_autorizada_por.staff.staff.last_name}.\n El siguiente paso del sistema: Generación de OC \n\n Este mensaje ha sido automáticamente generado por SAVIA VORDTEC',
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    to= ['ulises_huesc@hotmail.com',oc.req.orden.staff.staff.email],
                    headers={'Content-Type': 'text/html'}
                    )
                email.content_subtype = "html " # Importante para que se interprete como HTML
                email.send()
            except (BadHeaderError, SMTPException) as e:
                error_message = f'{usuario.staff.first_name}, Has generado la OC {oc.get_folio} correctamente pero el correo de notificación no ha sido enviado debido a un error: {e}'
                messages.warning(request, error_message)
            return redirect('requisicion-autorizada')


    context= {
        'proveedores':proveedores,
        'req':req,
        'form':form,
        'oc':oc,
        'productos':productos,
        'form_product':form_product,
        'tag':tag,
        'productos_comp':productos_comp,
        'subtotal':subtotal,
        'iva':iva,
        'total':total,
        'colaborador_sel':colaborador_sel,
        }
    return render(request, 'compras/oc.html',context)

@login_required(login_url='user-login')
def mostrar_comparativo(request, pk):
    comparativo = Comparativo.objects.get(id=pk)
    productos = Item_Comparativo.objects.filter(comparativo = comparativo)
    
    context= {
        'comparativo':comparativo,
        'productos':productos,
        }

    return render(request, 'compras/mostrar_comparativo.html',context)

@login_required(login_url='user-login')
def preevaluaciones(request, pk):
    proveedor = Proveedor.objects.get(id=pk)
    preevaluaciones= Preevaluacion.objects.filter(nombre = proveedor, completo = True)

    context = {
        'proveedor':proveedor,
        'preevaluaciones':preevaluaciones,
    }

    return render(request, 'compras/preevaluaciones.html',context)

@login_required(login_url='user-login')
def preevaluacion(request, pk):
    usuario = Profile.objects.get(staff__id=request.user.id)
    proveedor = Proveedor.objects.get(id=pk)
    preevaluacion, created = Preevaluacion.objects.get_or_create(nombre = proveedor, completo= False)
    form = PreevaluacionForm(instance = preevaluacion)
    error_messages = {}

    if request.method == 'POST':
        form = PreevaluacionForm(request.POST, instance = preevaluacion)
        if form.is_valid():
            preevaluacion = form.save(commit=False)
            preevaluacion.completo = True
            preevaluacion.creado_por = usuario
            preevaluacion.modified_at = datetime.now()
            preevaluacion.save()
            messages.success(request,f'Has creado la preevaluación con éxito')
            return redirect('dashboard-proveedores')
        else:
            for field, errors in form.errors.items():
                error_messages[field] = errors.as_text()

    
    context= {
        'proveedor': proveedor,
        'error_messages':error_messages,
        'form': form,
        }

    return render(request, 'compras/preevaluacion.html',context)

def autorizacion_preevaluacion(request):
    preevaluaciones = Preevaluacion.objects.filter(completo = True, resultado = None)

    context = {
        'preevaluaciones':preevaluaciones,
    }

    return render(request, 'compras/matriz_autorizacion_preevaluacion.html', context)

def autorizar_preevaluacion(request, pk):
    preevaluacion = Preevaluacion.objects.get(id = pk)

    if request.method == 'POST' and 'btn_autorizar' in request.POST:
        preevaluacion.resultado = True
        preevaluacion.save()
        messages.success(request,f'La preevaluacion {preevaluacion.id} ha sido autorizada')
        return redirect('autorizacion-preevaluacion')
    else:
        messages.success(request,'Nada')


    context = {
        'preevaluacion':preevaluacion,
    }

    return render(request, 'compras/autorizar_preevaluacion.html', context)


@login_required(login_url='user-login')
def matriz_oc(request):
    compras = Compra.objects.filter(complete=True)
    myfilter = CompraFilter(request.GET, queryset=compras)
    compras = myfilter.qs
    # Calcular el total de órdenes de compra
    total_de_oc = compras.count()
     # Calcular el número de OC que cumplen el criterio (created_at - approved_at <= 3)
    time_difference = ExpressionWrapper(F('created_at') - F('req__approved_at'), output_field=fields.DurationField())
    compras_con_criterio = compras.annotate(time_difference=time_difference).filter(time_difference__lte=timedelta(days=3))
    oc_cumplen = compras_con_criterio.count()

     # Calcular el indicador de cumplimiento (oc_cumplen / total_de_oc)
    if total_de_oc > 0:
        cumplimiento = (oc_cumplen / total_de_oc)*100
    else:
        cumplimiento = 0

     #Set up pagination
    p = Paginator(compras, 50)
    page = request.GET.get('page')
    compras_list = p.get_page(page)

    if request.method == 'POST' and 'btnReporte' in request.POST:
        return convert_excel_matriz_compras(compras)

    

    context= {
        'compras_list':compras_list,
        'compras':compras,
        'myfilter':myfilter,
        'cumplimiento': cumplimiento,
        }

    return render(request, 'compras/matriz_compras.html',context)

@login_required(login_url='user-login')
def matriz_oc_productos(request):
    compras = Compra.objects.filter(complete=True)
    articulos = ArticuloComprado.objects.filter(oc__complete = True).order_by('-oc__created_at')
    myfilter = ArticuloCompradoFilter(request.GET, queryset=articulos)
    articulos = myfilter.qs

    productos_optimized = articulos.select_related(
        'oc__req__orden__staff__staff',
        'oc__req__orden',
        'oc__req__orden__proyecto',
        'oc__req__orden__subproyecto',
        'oc__req__orden__area',
        'oc__proveedor__nombre',
        'producto__producto__articulos__producto__producto'
    ).only(
        'oc__folio',
        'oc__req__folio',
        'oc__req__orden__folio',
        'oc__req__orden__staff__staff__first_name',
        'oc__req__orden__staff__staff__last_name',
        'oc__req__orden__proyecto__nombre',
        'oc__req__orden__subproyecto__nombre',
        'created_at',
        'oc__proveedor__nombre__razon_social',
        'oc__req__orden__area__nombre',
        'cantidad',
        'producto__producto__articulos__producto__producto__codigo',
        'producto__producto__articulos__producto__producto__nombre',
        'precio_unitario',
        #'subtotal_parcial',
        #'iva_parcial',
        #'total'
    )



    #Set up pagination
    p = Paginator(articulos, 50)
    page = request.GET.get('page')
    articulos_list = p.get_page(page)

    if request.method == 'POST' and 'btnExcel' in request.POST:
        return convert_excel_solicitud_matriz_productos(productos_optimized)

    context= {
        'articulos_list':articulos_list,
        'articulos':articulos,
        'compras':compras,
        'myfilter':myfilter,
        }

    return render(request, 'compras/matriz_oc_productos.html',context)

@login_required(login_url='user-login')
def productos_oc(request, pk):
    compra = Compra.objects.get(id=pk)
    productos = ArticuloComprado.objects.filter(oc=compra)


    context = {
        'compra':compra,
        'productos':productos,
    }

    return render(request,'compras/oc_producto.html',context)

@login_required(login_url='user-login')
def upload_facturas(request, pk):
    pago = Pago.objects.get(id = pk)
    facturas = Facturas.objects.filter(pago = pago, hecho=True)
    factura, created = Facturas.objects.get_or_create(pago=pago, hecho=False)
    form = Facturas_Form()

    if request.method == 'POST':
        form = Facturas_Form(request.POST or None, request.FILES or None, instance = factura)
        factura = form.save(commit=False)
        factura.fecha_subido = date.today()
        factura.hora_subido = datetime.now().time()
        factura.hecho = True
        if form.is_valid():
            form.save()
            factura.save()
            messages.success(request,'Las facturas se subieron de manera exitosa')
            return redirect('matriz-compras')
        else:
            form = Facturas_Form()
            messages.error(request,'No se pudo subir tu documento')

    context={
        'facturas':facturas,
        'form':form,
        }

    return render(request, 'compras/upload.html', context)

@login_required(login_url='user-login')
def upload_xml(request, pk):
    compra = Compra.objects.get(id = pk)
    form = CompraFactForm()

    if request.method == 'POST':
        form = CompraFactForm(request.POST or None, request.FILES or None, instance = compra)
        if form.is_valid():
            form.save()
            return redirect('matriz-compras')
        else:
            form = CompraFactForm()
            messages.error(request,'No se pudo subir tu documento')

    context={
        'compra':compra,
        'form': form,
        }

    return render(request, 'compras/upload_xml.html', context)

@login_required(login_url='user-login')
def autorizacion_oc1(request):
    usuario = Profile.objects.get(staff__id=request.user.id)
    if usuario.tipo.oc_superintendencia == True:
        compras = Compra.objects.filter(complete=True, autorizado1= None).order_by('-folio')
    else:
        compras = Compra.objects.filter(flete=True,costo_fletes='1')
    #compras = Compra.objects.filter(complete=True, autorizado1= None).order_by('-folio')



    context= {
        'compras':compras,
        }

    return render(request, 'compras/autorizacion_oc1.html',context)

def cancelar_oc1(request, pk):
    usuario = Profile.objects.get(staff__id=request.user.id)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc = pk)

    if compra.costo_fletes == None:
        costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    if compra.tipo_de_cambio:
        costo_oc = compra.costo_oc * compra.tipo_de_cambio
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes * compra.tipo_de_cambio
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes
    costo_total = costo_fletes + costo_oc
    resta = compra.req.orden.subproyecto.presupuesto - costo_total - compra.req.orden.subproyecto.gastado
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)

    if request.method == 'POST':
        compra.oc_autorizada_por = usuario
        compra.autorizado1 = False
        compra.autorizado_date1 = date.today()
        compra.autorizado_hora1 = datetime.now().time()
        compra.save()
        messages.error(request,f'Has cancelado la compra con FOLIO: {compra.get_folio}')
        return redirect('autorizacion-oc1')

    context = {
        'compra':compra,
        'productos': productos,
        'costo_oc':costo_oc,
        'productos':productos,
        'tipo_cambio':compra.tipo_de_cambio,
        'resta':resta,
        'porcentaje':porcentaje,
        'costo_total':costo_total,
     }
    return render(request,'compras/cancelar_oc1.html', context)

def cancelar_oc2(request, pk):
    usuario = Profile.objects.get(staff__id=request.user.id)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc = pk)

    if compra.costo_fletes == None:
        costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    if compra.tipo_de_cambio:
        costo_oc = compra.costo_oc * compra.tipo_de_cambio
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes * compra.tipo_de_cambio
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes
    costo_total = costo_fletes + costo_oc
    resta = compra.req.orden.subproyecto.presupuesto - costo_total - compra.req.orden.subproyecto.gastado
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)


    if request.method == 'POST':
        compra.oc_autorizada_por2 = usuario
        compra.autorizado2 = False
        compra.autorizado_date2 = date.today()
        compra.autorizado_hora2 = datetime.now().time()
        compra.save()
        messages.error(request,f'Has cancelado la compra con FOLIO: {compra.get_folio}')
        return redirect('autorizacion-oc2')

    context = {
        'compra':compra,
        'productos': productos,
        'costo_oc':costo_oc,
        'productos':productos,
        'tipo_cambio':compra.tipo_de_cambio,
        'resta':resta,
        'porcentaje':porcentaje,
        'costo_total':costo_total,
     }
    return render(request,'compras/cancelar_oc2.html', context)

def back_oc(request, pk):
    perfil = Profile.objects.get(staff__id=request.user.id)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc = pk)
    #Traigo la requisición para poderla activar de nuevo
    requi = Requis.objects.get(id=compra.req.id)

    if compra.costo_fletes == None:
        costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    if compra.tipo_de_cambio:
        costo_oc = compra.costo_oc * compra.tipo_de_cambio
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes * compra.tipo_de_cambio
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes
    costo_total = costo_fletes + costo_oc
    resta = compra.req.orden.subproyecto.presupuesto - costo_total - compra.req.orden.subproyecto.gastado
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)

    form = Compra_ComentarioForm()

    if request.method == 'POST':
        form = Compra_ComentarioForm(request.POST, instance=compra)
        if form.is_valid():
            compra = form.save(commit = False)
            if not compra.autorizado1:
                compra.oc_autorizada_por = perfil
                compra.autorizado1 = None
                compra.complete = False
                compra.autorizado_date1 = date.today()
                compra.autorizado_hora1 = datetime.now().time()
                compra.regresar_oc = True
            else:
                compra.oc_autorizada_por2 = perfil
                compra.autorizado2 = None
                compra.autorizado1 = None
                compra.complete = False
                compra.autorizado_date2 = date.today()
                compra.autorizado_hora2 = datetime.now().time()
                compra.regresar_oc = True
            #Esta línea es la que activa a la requi
            #requi.colocada = False
            compra.save()
            #requi.save()
            messages.success(request,f'Has regresado la compra con FOLIO: {compra.get_folio} y ahora podrás encontrar esos productos en el apartado devolución')
            return redirect('compras-devueltas')

    context = {
        'form':form,
        'compra':compra,
        'productos': productos,
        'costo_oc':costo_oc,
        'productos':productos,
        'tipo_cambio':compra.tipo_de_cambio,
        'resta':resta,
        'porcentaje':porcentaje,
        'costo_total':costo_total,
     }

    return render(request,'compras/back_oc.html', context)




def autorizar_oc1(request, pk):
    usuario = Profile.objects.get(staff__id=request.user.id)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc=pk)
    # Esto asume que ya has obtenido una instancia específica de Compra con 'compra = Compra.objects.get(id=pk)'
    proyecto_id = compra.req.orden.proyecto.id
    #print('proyecto',proyecto_id)
    compras_por_sumar = Compra.objects.filter(req__orden__proyecto__id=proyecto_id, complete = True)
    # Ahora, sumamos los 'costo_oc' para todas las Compras que están bajo el mismo proyecto.
    total_costo_oc = 0
    total_costo_autorizado = 0
    total_costo_pagado = 0
    # Recorremos cada compra para calcular los totales.
    for compra in compras_por_sumar:
        # Ajustamos el costo_oc si la moneda es DOLARES.
        if compra.moneda:
            if compra.moneda.nombre == "DOLARES":
                costo_oc = compra.costo_oc
                tc = compra.tipo_de_cambio or 17            
                costo_oc_ajustado = compra.costo_oc * tc

            else:
                costo_oc_ajustado = compra.costo_oc
        else:
            costo_oc_ajustado = compra.costo_oc
        
        # Sumamos al total general.
        total_costo_oc += costo_oc_ajustado
        
        # Si la compra está autorizada, la sumamos al total autorizado.
        if compra.autorizado2:
            total_costo_autorizado += costo_oc_ajustado
        
        # Si la compra está pagada, la sumamos al total pagado.
        if compra.pagada:
            total_costo_pagado += costo_oc_ajustado

    # Ahora tenemos los totales calculados.
    #print('Total costo OC:', total_costo_oc)
    #print('Total costo OC (autorizado):', total_costo_autorizado)
    #print('Total costo OC (pagado):', total_costo_pagado)

    costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    
    if compra.tipo_de_cambio:
        costo_oc = compra.costo_oc * compra.tipo_de_cambio
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes * compra.tipo_de_cambio
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes

    print(costo_oc)
    print(compra.req.orden.subproyecto.gastado)
    
    costo_total = costo_fletes + costo_oc 
    resta = compra.req.orden.subproyecto.presupuesto - total_costo_pagado - costo_total
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)


    if request.method == 'POST':
        compra.autorizado1 = True
        compra.oc_autorizada_por = usuario
        compra.autorizado_date1 = date.today()
        compra.autorizado_hora1 = datetime.now().time()
        compra.save()
        static_path = settings.STATIC_ROOT
        img_path = os.path.join(static_path,'images','SAVIA_Logo.png')
        img_path2 = os.path.join(static_path,'images','logo vordtec_documento.png')
        image_base64 = get_image_base64(img_path)
        logo_v_base64 = get_image_base64(img_path2)
        html_message = f"""
            <html>
                <head>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <p><img src="data:image/jpeg;base64,{logo_v_base64}" alt="Imagen" style="width:100px;height:auto;"/></p>
                    <p>Estimado {compra.req.orden.staff.staff.first_name} {compra.req.orden.staff.staff.last_name},</p>
                    <p>Estás recibiendo este correo porque tu OC {compra.get_folio} | RQ: {compra.req.folio} |Sol: {compra.req.orden.folio} ha sido autorizada por {compra.oc_autorizada_por.staff.staff.first_name} {compra.oc_autorizada_por.staff.staff.last_name},</p>
                    <p>El siguiente paso del sistema: Autorización de OC por Gerencia de Planta</p>
                    <p><img src="data:image/png;base64,{image_base64}" alt="Imagen" style="width:50px;height:auto;border-radius:50%"/></p>
                    <p>Este mensaje ha sido automáticamente generado por SAVIA 2.0</p>
                </body>
            </html>
        """
        try:
            email = EmailMessage(
                f'OC Autorizada {compra.get_folio}|RQ: {compra.req.folio} |Sol: {compra.req.orden.folio}',
                body=html_message,
                from_email = settings.DEFAULT_FROM_EMAIL,
                to= ['ulises_huesc@hotmail.com',compra.req.orden.staff.staff.email],
                headers={'Content-Type': 'text/html'}
                )
            email.content_subtype = "html " # Importante para que se interprete como HTML
            email.send()
            messages.success(request, f'{usuario.staff.first_name} has autorizado la solicitud {compra.get_folio}')
        except (BadHeaderError, SMTPException) as e:
            error_message = f'{usuario.staff.first_name} has autorizado la compra {compra.get_folio} pero el correo de notificación no ha sido enviado debido a un error: {e}'
            messages.success(request, error_message)  
        return redirect('autorizacion-oc1')

    context={
        'compra':compra,
        'costo_oc':costo_oc,
        'productos':productos,
        'tipo_cambio':compra.tipo_de_cambio,
        'resta':resta,
        'porcentaje':porcentaje,
        'costo_total':costo_total,
        }

    return render(request, 'compras/autorizar_oc1.html',context)

@login_required(login_url='user-login')
def autorizacion_oc2(request):
    usuario = Profile.objects.get(staff__id=request.user.id)
    #if usuario.tipo.oc_gerencia == True:
    #    compras = Compra.objects.filter(complete = True, autorizado1 = True, autorizado2= None).order_by('-folio')
    #else:
    #    compras = Compra.objects.filter(flete=True,costo_fletes='1')
    compras = Compra.objects.filter(complete = True, autorizado1 = True, autorizado2= None).order_by('-folio')

    context= {
        'compras':compras,
        }

    return render(request, 'compras/autorizacion_oc2.html',context)


def autorizar_oc2(request, pk):
    usuario = Profile.objects.get(staff__id=request.user.id)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc=pk)
    proyecto_id = compra.req.orden.proyecto.id
    #print('proyecto',proyecto_id)
    compras_por_sumar = Compra.objects.filter(req__orden__proyecto__id=proyecto_id, complete = True)
    # Ahora, sumamos los 'costo_oc' para todas las Compras que están bajo el mismo proyecto.
    total_costo_oc = 0
    total_costo_autorizado = 0
    total_costo_pagado = 0
    # Recorremos cada compra para calcular los totales.
    for compra in compras_por_sumar:
        # Ajustamos el costo_oc si la moneda es DOLARES.
        if compra.moneda:
            if compra.moneda.nombre == "DOLARES":
                costo_oc = compra.costo_oc
                tc = compra.tipo_de_cambio or 17            
                costo_oc_ajustado = compra.costo_oc * tc

            else:
                costo_oc_ajustado = compra.costo_oc
        else:
            costo_oc_ajustado = compra.costo_oc
        
        # Sumamos al total general.
        total_costo_oc += costo_oc_ajustado
        
        # Si la compra está autorizada, la sumamos al total autorizado.
        if compra.autorizado2:
            total_costo_autorizado += costo_oc_ajustado
        
        # Si la compra está pagada, la sumamos al total pagado.
        if compra.pagada:
            total_costo_pagado += costo_oc_ajustado

    # Ahora tenemos los totales calculados.
    #print('Total costo OC:', total_costo_oc)
    #print('Total costo OC (autorizado):', total_costo_autorizado)
    #print('Total costo OC (pagado):', total_costo_pagado)

    costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    if compra.tipo_de_cambio:
        costo_oc = compra.costo_oc * compra.tipo_de_cambio
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes * compra.tipo_de_cambio
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes
    costo_total = costo_fletes + costo_oc
    resta = compra.req.orden.subproyecto.presupuesto - total_costo_pagado - costo_total
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)

    if request.method == 'POST':
        compra.autorizado2 = True
        compra.oc_autorizada_por2 = usuario
        compra.autorizado_date2 = date.today()
        compra.autorizado_hora2 = datetime.now().time()
        compra.save()
        archivo_oc = attach_oc_pdf(request, compra.id)
        static_path = settings.STATIC_ROOT
        img_path = os.path.join(static_path,'images','SAVIA_Logo.png')
        img_path2 = os.path.join(static_path,'images','logo vordtec_documento.png')
        image_base64 = get_image_base64(img_path)
        logo_v_base64 = get_image_base64(img_path2)
        if compra.cond_de_pago.nombre == "CREDITO":
            html_message2 = f"""
                <html>
                    <head>
                        <meta charset="UTF-8">
                    </head>
                    <body>
                        <p>Estimado(a) {compra.proveedor.contacto}| Proveedor {compra.proveedor.nombre}:,</p>
                        <p>Estás recibiendo este correo porque has sido seleccionado para surtirnos la OC adjunta con folio: {compra.folio}.<p>
                        <p>&nbsp;</p>
                        <p> Atte. {compra.creada_por.staff.first_name} {compra.creada_por.staff.last_name}</p> 
                        <p>GRUPO VORDCAB S.A. de C.V.</p>
                        <p><img src="data:image/jpeg;base64,{logo_v_base64}" alt="Imagen" style="width:100px;height:auto;"/></p>
                        <p><img src="data:image/png;base64,{image_base64}" alt="Imagen" style="width:50px;height:auto;border-radius:50%"/></p>
                        <p>Este mensaje ha sido automáticamente generado por SAVIA 2.0</p>
                    </body>
                </html>
            """
            try:
                email = EmailMessage(
                f'Compra Autorizada {compra.get_folio}|SAVIA',
                body=html_message2,
                from_email =settings.DEFAULT_FROM_EMAIL,
                to= ['ulises_huesc@hotmail.com', compra.creada_por.staff.email, compra.proveedor.email],
                headers={'Content-Type': 'text/html'}
                )
                email.content_subtype = "html " # Importante para que se interprete como HTML
                email.attach(f'folio:{compra.get_folio}.pdf',archivo_oc,'application/pdf')
                email.send()
            except (BadHeaderError, SMTPException) as e:
                error_message = f'correo de notificación no ha sido enviado debido a un error: {e}'
            html_message = f"""
                <html>
                    <head>
                        <meta charset="UTF-8">
                    </head>
                    <body>
                        <p><img src="data:image/jpeg;base64,{logo_v_base64}" alt="Imagen" style="width:100px;height:auto;"/></p>
                        <p>Estimado {compra.req.orden.staff.staff.first_name} {compra.req.orden.staff.staff.last_name},</p>
                        <p>Estás recibiendo este correo porque tu OC {compra.get_folio} | RQ: {compra.req.folio} |Sol: {compra.req.orden.folio} ha sido autorizada por {compra.oc_autorizada_por2.staff.staff.first_name} {compra.oc_autorizada_por2.staff.staff.last_name},</p>
                        <p>El siguiente paso del sistema: Recepción por parte de Almacén |Compra a crédito</p>
                        <p><img src="data:image/png;base64,{image_base64}" alt="Imagen" style="width:50px;height:auto;border-radius:50%"/></p>
                        <p>Este mensaje ha sido automáticamente generado por SAVIA 2.0</p>
                    </body>
                </html>
            """
            try:
                email = EmailMessage(
                    f'OC Autorizada Gerencia {compra.get_folio}|RQ: {compra.req.folio} |Sol: {compra.req.orden.folio}',
                    body=html_message,
                    #f'Estimado {requi.orden.staff.staff.staff.first_name} {requi.orden.staff.staff.staff.last_name},\n Estás recibiendo este correo porque tu solicitud: {requi.orden.folio}| Req: {requi.folio} ha sido autorizada,\n por {requi.requi_autorizada_por.staff.staff.first_name} {requi.requi_autorizada_por.staff.staff.last_name}.\n El siguiente paso del sistema: Generación de OC \n\n Este mensaje ha sido automáticamente generado por SAVIA VORDTEC',
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    to= ['ulises_huesc@hotmail.com',],#[requi.orden.staff.staff.staff.email],
                    headers={'Content-Type': 'text/html'}
                    )
                email.content_subtype = "html " # Importante para que se interprete como HTML
                email.send()
                for producto in productos:
                    if producto.producto.producto.articulos.producto.producto.especialista == True:
                        archivo_oc = attach_oc_pdf(request, compra.id)
                        email = EmailMessage(
                            f'Compra Autorizada {compra.get_folio}',
                            f'Estimado proveedor,\n Estás recibiendo este correo porque ha sido aprobada una OC que contiene el producto código:{producto.producto.producto.articulos.producto.producto.codigo} descripción:{producto.producto.producto.articulos.producto.producto.nombre} el cual requiere la liberación de calidad\n Este mensaje ha sido automáticamente generado por SAVIA X',
                            settings.DEFAULT_FROM_EMAIL,
                            ['ulises_huesc@hotmail.com',],
                            )
                        email.attach(f'folio:{compra.get_folio}.pdf',archivo_oc,'application/pdf')
                        email.send()
                messages.success(request, f'{usuario.staff.first_name} has autorizado la solicitud {compra.get_folio}')
            except (BadHeaderError, SMTPException) as e:
                error_message = f'{usuario.staff.staff.first_name} has autorizado la compra {compra.folio} pero el correo de notificación no ha sido enviado debido a un error: {e}'
                messages.warning(request, error_message)   
        else:
            html_message = f"""
                    <html>
                        <head>
                            <meta charset="UTF-8">
                        </head>
                        <body>
                            <p><img src="data:image/jpeg;base64,{logo_v_base64}" alt="Imagen" style="width:100px;height:auto;"/></p>
                            <p>Estimado {compra.req.orden.staff.staff.first_name} {compra.req.orden.staff.staff.last_name},</p>
                            <p>Estás recibiendo este correo porque tu OC {compra.get_folio} | RQ: {compra.req.folio} |Sol: {compra.req.orden.folio} ha sido autorizada por {compra.oc_autorizada_por2.staff.staff.first_name} {compra.oc_autorizada_por2.staff.staff.last_name},</p>
                            <p>El siguiente paso del sistema: Pago por parte de tesorería</p>
                            <p><img src="data:image/png;base64,{image_base64}" alt="Imagen" style="width:50px;height:auto;border-radius:50%"/></p>
                            <p>Este mensaje ha sido automáticamente generado por SAVIA 2.0</p>
                        </body>
                    </html>
                """
            try:
                email = EmailMessage(
                    f'OC Autorizada Gerencia {compra.get_folio}|RQ: {compra.req.folio} |Sol: {compra.req.orden.folio}',
                    body=html_message,
                    #f'Estimado {requi.orden.staff.staff.staff.first_name} {requi.orden.staff.staff.staff.last_name},\n Estás recibiendo este correo porque tu solicitud: {requi.orden.folio}| Req: {requi.folio} ha sido autorizada,\n por {requi.requi_autorizada_por.staff.staff.first_name} {requi.requi_autorizada_por.staff.staff.last_name}.\n El siguiente paso del sistema: Generación de OC \n\n Este mensaje ha sido automáticamente generado por SAVIA VORDTEC',
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    to= ['ulises_huesc@hotmail.com'],#[requi.orden.staff.staff.staff.email],
                    headers={'Content-Type': 'text/html'}
                    )
                email.content_subtype = "html " # Importante para que se interprete como HTML
                email.send()
                messages.success(request, f'{usuario.staff.staff.first_name} has autorizado la compra {compra.get_folio}')
            except (BadHeaderError, SMTPException) as e:
                error_message = f'{usuario.staff.staff.first_name} has autorizado la compra {compra.get_folio} pero el correo de notificación no ha sido enviado debido a un error: {e}'
                messages.warning(request, error_message)   
        return redirect('autorizacion-oc2')

    context={
        'compra':compra,
        'costo_oc':costo_oc,
        'productos':productos,
        'tipo_cambio':compra.tipo_de_cambio,
        'resta':resta,
        'porcentaje':porcentaje,
        'costo_total':costo_total,
        }

    return render(request, 'compras/autorizar_oc2.html',context)

def comparativos(request):
    comparativos = Comparativo.objects.filter(completo = True)
    
    context= {
        'comparativos':comparativos,
    }
    return render(request,'compras/comparativos.html', context)

@login_required(login_url='user-login')
def crear_comparativo(request):
    usuario = Profile.objects.get(staff__id=request.user.id)
    #Tengo que revisar primero si ya existe una orden pendiente del usuario
    
    comparativo, created = Comparativo.objects.get_or_create(completo= False, creada_por=usuario)
    
    productos = Item_Comparativo.objects.filter(comparativo = comparativo, completo = True)

    proveedores = Proveedor_direcciones.objects.all()
    articulos = Inventario.objects.all()
    form_item = Item_ComparativoForm()
    form = ComparativoForm()

    if request.method =='POST':
        if "btn_agregar" in request.POST:
            form = ComparativoForm(request.POST, request.FILES or None, instance=comparativo)
            #abrev= usuario.distrito.abreviado
            if form.is_valid():
                comparativo = form.save(commit=False)
                comparativo.completo = True
                comparativo.created_at = date.today()
                #comparativo.created_at_time = datetime.now().time()
                comparativo.creado_por =  usuario
                comparativo.save()
                #form.save()
                messages.success(request, f'El comparativo {comparativo.id} ha sido creado')
                return redirect('comparativos')
        if "btn_producto" in request.POST:
            articulo, created = Item_Comparativo.objects.get_or_create(completo = False, comparativo = comparativo)
            form_item = Item_ComparativoForm(request.POST, instance=articulo)
            if form_item.is_valid():
                articulo = form_item.save(commit=False)
                articulo.completo = True
                articulo.save()
                messages.success(request, 'Se ha agregado el artículo exitosamente')
                return redirect('crear_comparativo')
        
    context= {
        'productos':productos,
        'form':form,
        'form_item':form_item,
        'articulos':articulos,
        'comparativo':comparativo,
        'proveedores':proveedores,
    }

    return render(request, 'compras/crear_comparativo.html', context)

@login_required(login_url='user-login')
def editar_comparativo(request, pk):
    usuario = Profile.objects.get(staff__id=request.user.id)
    comparativo =Comparativo.objects.get(id = pk)
    productos = Item_Comparativo.objects.filter(comparativo = comparativo, completo = True)
    proveedores = Proveedor_direcciones.objects.all()
    articulos = Inventario.objects.all()
    form_item = Item_ComparativoForm()
    form = ComparativoForm(instance = comparativo)

    if request.method =='POST':
        if "btn_agregar" in request.POST:
            form = ComparativoForm(request.POST, request.FILES, instance = comparativo)
            #abrev= usuario.distrito.abreviado
            if form.is_valid():
                comparativo = form.save(commit=False)
                comparativo.completo = True
                comparativo.created_at = date.today()
                #comparativo.created_at_time = datetime.now().time()
                comparativo.creado_por =  usuario
                comparativo.save()
                #form.save()
                messages.success(request, f'El comparativo {comparativo.id} ha sido modificado')
                return redirect('comparativos')
        if "btn_producto" in request.POST:
            articulo, created = Item_Comparativo.objects.get_or_create(completo = False, comparativo = comparativo)
            form_item = Item_ComparativoForm(request.POST, instance=articulo)
            if form_item.is_valid():
                articulo = form_item.save(commit=False)
                articulo.completo = True
                articulo.save()
                messages.success(request, 'Se ha agregado el artículo exitosamente')
                return redirect('editar-comparativo')
        
    context= {
        'productos':productos,
        'form':form,
        'form_item':form_item,
        'articulos':articulos,
        'comparativo':comparativo,
        'proveedores':proveedores,
    }

    return render(request, 'compras/actualizar_comparativo.html', context)

def articulos_comparativo(request, pk):
    articulos = Item_Comparativo.objects.filter(comparativo__id = pk , completo = True)

    context= {
        'articulos':articulos,
    }
    return render(request, 'compras/articulos_comparativo.html', context)

def articulo_comparativo_delete(request, pk):
   
    articulo = Item_Comparativo.objects.get(id=pk)
    comparativo = articulo.comparativo.id
   
    messages.success(request,f'El articulo ha sido eliminado exitosamente')
    articulo.delete()

    return redirect('crear_comparativo')

@login_required(login_url='user-login')
def historico_articulos_compras(request):
    registros = ArticuloComprado.history.all()

    myfilter = HistoricalArticuloCompradoFilter(request.GET, queryset=registros)
    registros = myfilter.qs

    #Set up pagination
    p = Paginator(registros, 30)
    page = request.GET.get('page')
    registros_list = p.get_page(page)

    context = {
        'registros_list':registros_list,
        'myfilter':myfilter,
        }

    return render(request,'compras/historico_articulos_comprados.html',context)

def descargar_pdf(request, pk):
    compra = get_object_or_404(Compra, id=pk)
    buf = generar_pdf(compra)
    return FileResponse(buf, as_attachment=True, filename='oc_' + str(compra.id) + '.pdf')

def attach_oc_pdf(request, pk):
    compra = get_object_or_404(Compra, id=pk)
    buf = generar_pdf(compra)

    # Si en algún lugar más de tu código necesitas hacer más cosas antes de retornar buf.getvalue(),
    # entonces aquí es el lugar para hacerlo. Por ahora, sólo retornaremos el valor.

    return buf.getvalue()


def generar_pdf(compra):
    #Configuration of the PDF object
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    #doc = SimpleDocTemplate(buf, pagesize=letter)
    #Here ends conf.
    #compra = Compra.objects.get(id=pk)
    productos = ArticuloComprado.objects.filter(oc=compra.id)

    #Azul Vordcab
    prussian_blue = Color(0.0859375,0.1953125,0.30859375)
    rojo = Color(0.59375, 0.05859375, 0.05859375)
    #Encabezado
    c.setFillColor(black)
    c.setLineWidth(.2)
    c.setFont('Helvetica',8)
    caja_iso = 760
    #Elaborar caja
    #c.line(caja_iso,500,caja_iso,720)



    c.drawString(410,caja_iso + 10,'Preparado por:')
    c.drawString(410,caja_iso,'Adquisiciones')
    c.drawString(500,caja_iso + 10,'Aprobación')
    c.drawString(475,caja_iso,'Subdirección Administrativa')
    c.drawString(20,caja_iso-20,'Número de documento')
    c.drawString(30,caja_iso-30,'F-ADQ-N4-01.02')
    c.drawString(145,caja_iso-20,'Clasificación del documento')
    c.drawString(175,caja_iso-30,'Registro')
    c.drawString(255,caja_iso-20,'Nivel del documento')
    c.drawString(280,caja_iso-30, 'N5')
    c.drawString(340,caja_iso-20,'Revisión No.')
    c.drawString(352,caja_iso-30,'001')
    c.drawString(410,caja_iso-20,'Fecha de Emisión')
    c.drawString(425,caja_iso-30,'')
    c.drawString(500,caja_iso-20,'Fecha de Modificación')
    c.drawString(525,caja_iso-30,'')

    caja_proveedor = caja_iso - 50
    c.setFont('Helvetica',12)
    c.setFillColor(prussian_blue)
    # REC (Dist del eje Y, Dist del eje X, LARGO DEL RECT, ANCHO DEL RECT)
    c.rect(150,750,250,30, fill=True, stroke=False) #Barra azul superior Orden de Compra
    c.rect(20,caja_proveedor,565,10, fill=True, stroke=False) #Barra azul superior Proveedor | Detalle
    c.rect(20,570,565,2, fill=True, stroke=False) #Linea posterior horizontal
    c.setFillColor(white)
    c.setLineWidth(.2)
    c.setFont('Helvetica-Bold',14)
    c.drawCentredString(280,760,'Orden de compra')
    c.setLineWidth(.3) #Grosor
    c.line(20,caja_proveedor,20,570) #Eje Y donde empieza, Eje X donde empieza, donde termina eje y,donde termina eje x (LINEA 1 contorno)
    c.line(585,caja_proveedor,585,570) #Linea 2 contorno
    c.drawInlineImage('static/images/logo vordtec_documento.png',40,755, 1.5 * cm, 0.75 * cm) #Imagen vortec

    c.setFillColor(white)
    c.setFont('Helvetica-Bold',9)
    c.drawString(120,caja_proveedor+1,'Autorización')
    c.drawString(400,caja_proveedor+1, 'Datos de Proveedor')
    inicio_central = 300
    c.line(inicio_central,caja_proveedor,inicio_central,570) #Linea Central de caja Proveedor | Detalle
    c.setFillColor(black)
    c.setFont('Helvetica',8)
    c.drawRightString(130,caja_proveedor-10,'Folio de solicitud:')
    c.drawRightString(130,caja_proveedor-20,'Folio de Requisición:')
    c.drawRightString(130,caja_proveedor-30,'Folio de orden de compra:')
    c.drawRightString(130,caja_proveedor-40,'Proyecto/Orden de Trabajo:')
    c.drawRightString(130,caja_proveedor-50,'Subproyecto:')
    c.drawRightString(130,caja_proveedor-60,'Elaboró:')
    c.drawRightString(130,caja_proveedor-70,'Autorizó:')
    c.drawRightString(130,caja_proveedor-80,'Fecha:')

    c.drawString(135,caja_proveedor-10, compra.req.orden.folio)
    c.drawString(135,caja_proveedor-20, compra.req.folio)
    c.drawString(135,caja_proveedor-30, compra.get_folio) #podría ser folio también
    c.drawString(135,caja_proveedor-40, compra.req.orden.proyecto.nombre)
    c.drawString(135,caja_proveedor-50, compra.req.orden.subproyecto.nombre)
    c.drawString(135,caja_proveedor-60, compra.req.orden.staff.staff.first_name+' '+compra.req.orden.staff.staff.last_name)
    if compra.oc_autorizada_por2:
        c.drawString(135,caja_proveedor-70, compra.oc_autorizada_por2.staff.first_name+' '+ compra.oc_autorizada_por2.staff.last_name)
    c.drawString(135,caja_proveedor-80, str(compra.autorizado_date2))

    c.setFillColor(black)
    c.setFont('Helvetica',8)
    c.drawRightString(inicio_central + 110,caja_proveedor-10,'Nombre:')
    c.drawRightString(inicio_central + 110,caja_proveedor-20,'RFC:')
    c.drawRightString(inicio_central + 110,caja_proveedor-30,'Número de Cuenta Bancaria:')
    c.drawRightString(inicio_central + 110,caja_proveedor-40,'Nombre del Banco:')
    c.drawRightString(inicio_central + 110,caja_proveedor-50,'CLABE:')
    c.drawRightString(inicio_central + 110,caja_proveedor-60,'SWIFT:')
    c.drawRightString(inicio_central + 110,caja_proveedor-70,'Estatus:')

    c.drawString(inicio_central + 115,caja_proveedor-10, compra.proveedor.nombre.razon_social)
    c.drawString(inicio_central + 115,caja_proveedor-20, compra.proveedor.nombre.rfc)
    c.drawString(inicio_central + 115,caja_proveedor-30, compra.proveedor.cuenta)
    c.drawString(inicio_central + 115,caja_proveedor-40, compra.proveedor.banco.nombre)
    c.drawString(inicio_central + 115,caja_proveedor-50, compra.proveedor.clabe)
    if compra.proveedor.swift:
        c.drawString(inicio_central + 115,caja_proveedor-60, compra.proveedor.swift)
    c.drawString(inicio_central + 115,caja_proveedor-70, compra.proveedor.estatus.nombre)

    c.setFont('Helvetica',12)
    c.setFillColor(prussian_blue)
    c.rect(20,caja_proveedor-90,565,10, fill=True, stroke=False)

    c.setFillColor(white)
    c.setFont('Helvetica-Bold',9)
    c.drawString(90,caja_proveedor-89,'Condiciones Comerciales')
    c.drawString(370,caja_proveedor-89, 'Datos de Facturación')

    c.setFillColor(black)
    c.setFont('Helvetica',8)
    c.drawRightString(130,caja_proveedor-100,'Tiempo de entrega:')
    c.drawRightString(130,caja_proveedor-110,'Política de Garantía:')
    c.drawRightString(130,caja_proveedor-120,'Condición de pago:')
    c.drawRightString(130,caja_proveedor-130,'Vigencia de cotización:')

    
    c.drawString(135,caja_proveedor-100, str(compra.dias_de_entrega))
    #c.drawString(135,caja_proveedor-110, compra.uso_del_cfdi.descripcion)
    c.drawString(135,caja_proveedor-120, compra.cond_de_pago.nombre )
    #c.drawString(135,caja_proveedor-130, compra.uso_del_cfdi.descripcion)


    c.drawRightString(inicio_central + 110,caja_proveedor-100,'Moneda:')
    c.drawRightString(inicio_central + 110,caja_proveedor-110,'Uso del CFDI:')
    c.drawRightString(inicio_central + 110,caja_proveedor-120,'Enviar factura al correo:')
    c.drawRightString(inicio_central + 110,caja_proveedor-130,'Regimen Fiscal:')
   
    c.drawString(inicio_central + 115,caja_proveedor-100, compra.moneda.nombre)
    c.drawString(inicio_central + 115,caja_proveedor-110, compra.uso_del_cfdi.descripcion)
    c.drawString(inicio_central + 115,caja_proveedor-120, compra.creada_por.staff.email)
    c.drawString(inicio_central + 115,caja_proveedor-130, '601 - General de Ley Personas Morales')

    data =[]
    data_c = []
    high = 530
    item = 0
    
    data.append(['''Partida''','''Código''','''Descripción General''', '''Cantidad''', '''Unidad''', '''P.Unitario''', '''Descuento''', '''Importe'''])
   
    for producto in productos:
        item = item + 1
        importe = producto.precio_unitario * producto.cantidad
        importe_rounded = round(importe, 4)
        data.append([
            item,
            producto.producto.producto.articulos.producto.producto.codigo,
            producto.producto.producto.articulos.producto.producto.nombre,
            producto.cantidad, 
            producto.producto.producto.articulos.producto.producto.unidad,
            producto.precio_unitario,
            '',
            importe_rounded
        ])
        high = high - 18

    c.setFillColor(black)
    c.setFont('Helvetica',8)

    c.setFillColor(prussian_blue)
    # REC (Dist del eje Y, Dist del eje X, LARGO DEL RECT, ANCHO DEL RECT)
    c.rect(20,210,390,10, fill=True, stroke=False) #2ra linea azul, donde esta el proyecto y el subproyecto, se coloca altura de 150
    c.setFillColor(black)
    c.setFillColor(white)
    c.setLineWidth(.1)
    c.setFont('Helvetica-Bold',10)
    c.drawString(200,211,'Total con letra')

   

    
    c.setLineWidth(.3)
    c.line(410,220,410,160) #Eje Y donde empieza, Eje X donde empieza, donde termina eje y,donde termina eje x (LINEA 1 contorno)
    c.line(410,160,580,160)

    c.setFillColor(black)
    c.setFont('Helvetica-Bold',9)

    montos_align = 480
    c.drawRightString(montos_align,210,'Sub Total:')
    c.drawRightString(montos_align,200,'IVA 16%:')
    c.drawRightString(montos_align,190,'Importe Neto:')
    c.drawRightString(montos_align,180,'Costo fletes:')
    c.setFillColor(prussian_blue)
    c.setFillColor(black)
    c.drawString(20,130,'Opciones y condiciones:')
    c.setFont('Helvetica',8)
    letras = 320
    #c.drawString(20,140,'Total con letra:')
    #c.line(135,90,215,90 ) #Linea de Autorizacion
    #c.line(350,90,430,90)
    c.drawCentredString(175,70,'Autorización')
    c.drawCentredString(390,70,'Autorización')

    c.drawCentredString(175,80,'Superintendente Administrativo')
    c.drawCentredString(390,80,'Gerencia Zona')
    c.setFont('Helvetica-Bold',8)
    if compra.autorizado1:
        c.drawCentredString(175,90,compra.oc_autorizada_por.staff.first_name + ' ' +compra.oc_autorizada_por.staff.last_name)
    if compra.autorizado2:
        c.drawCentredString(390,90,compra.oc_autorizada_por2.staff.first_name + ' ' + compra.oc_autorizada_por2.staff.last_name)

    c.setFont('Helvetica',10)
    subtotal = compra.costo_oc - compra.costo_iva
    c.drawRightString(montos_align + 90,210,'$ ' + str(subtotal))
    c.drawRightString(montos_align + 90,200,'$ ' + str(compra.costo_iva))
    c.drawRightString(montos_align + 90,190,'$ ' + str(compra.costo_oc))
    if compra.costo_fletes is None:
        compra.costo_fletes = 0

    c.drawRightString(montos_align + 90,180,'$ ' + str(compra.costo_fletes))
    c.setFillColor(prussian_blue)

    if compra.impuesto:
        c.setFillColor(black)
        c.setFont('Helvetica-Bold',9)
        c.drawRightString(montos_align,170,'Impuestos Adicionales:')
        c.setFont('Helvetica',10)
        c.drawRightString(montos_align + 90,170,'$ ' + str(compra.impuestos_adicionales))
        c.setFillColor(prussian_blue)
        c.drawRightString(montos_align,160,'Total:')
        c.drawRightString(montos_align + 90,160,'$ ' + str(compra.costo_plus_adicionales))
    else:
        c.drawRightString(montos_align,170,'Total:')
        c.drawRightString(montos_align + 90,170,'$ ' + str(compra.costo_plus_adicionales))
    c.setFont('Helvetica', 9)




    if compra.moneda.nombre == "PESOS":
        c.drawString(40,201, num2words(compra.costo_plus_adicionales, lang='es', to='currency', currency='MXN'))
    if compra.moneda.nombre == "DOLARES":
        c.drawString(40,201, num2words(compra.costo_plus_adicionales, lang='es', to='currency',currency='USD'))

    c.setFillColor(black)
    width, height = letter
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]

    if compra.opciones_condiciones is not None:
        options_conditions = compra.opciones_condiciones
    else:
        options_conditions = "NA"

    options_conditions_paragraph = Paragraph(options_conditions, styleN)


    # Crear un marco (frame) en la posición específica
    frame = Frame(135, 0, width-145, height-648, id='normal')

    # Agregar el párrafo al marco
    frame.addFromList([options_conditions_paragraph], c)
    c.setFillColor(prussian_blue)
    c.rect(20,30,565,30, fill=True, stroke=False)
    c.setFillColor(white)

    
    table = Table(data, colWidths=[1 * cm, 1.2 * cm, 10 * cm, 1.5 * cm, 1.2 * cm, 1.5 * cm,1.5 * cm, 1.5 * cm,])
    table_style = TableStyle([ #estilos de la tabla
        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.white),
        ('BOX',(0,0),(-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        #ENCABEZADO
        ('TEXTCOLOR',(0,0),(-1,0), white),
        ('FONTSIZE',(0,0),(-1,0), 7),
        ('BACKGROUND',(0,0),(-1,0), prussian_blue),
        #CUERPO
        ('TEXTCOLOR',(0,1),(-1,-1), colors.black),
        ('FONTSIZE',(0,1),(-1,-1), 6),
        ])
    table_style2 = TableStyle([ #estilos de la tabla
        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.white),
        ('BOX',(0,0),(-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        #ENCABEZADO
        ('TEXTCOLOR',(0,0),(-1,0), colors.black),
        ('FONTSIZE',(0,0),(-1,0), 6),
        #('BACKGROUND',(0,0),(-1,0), prussian_blue),
        #CUERPO
        ('TEXTCOLOR',(0,1),(-1,-1), colors.black),
        ('FONTSIZE',(0,1),(-1,-1), 6),
        ])
    table.setStyle(table_style)

  

    rows_per_page = 15
    total_rows = len(data) - 1  # Excluye el encabezado
    remaining_rows = total_rows - rows_per_page

     
    if remaining_rows <= 0:
        # Si no hay suficientes filas para una segunda página, dibujar la tabla completa en la primera página
        table.wrapOn(c, c._pagesize[0], c._pagesize[1])
        table.drawOn(c, 20, high)  # Posición en la primera página
    else:
        # Dibujar las primeras 15 filas en la primera página
        first_page_data = data[:rows_per_page + 1]  # Incluye el encabezado
        first_page_table = Table(first_page_data, colWidths=[1 * cm, 1.2 * cm, 10 * cm, 1.5 * cm, 1.2 * cm, 1.5 * cm,1.5 * cm, 1.5 * cm,])
        first_page_table.setStyle(table_style)
        first_page_table.wrapOn(c, c._pagesize[0], c._pagesize[1])
        #adjusted_high = c._pagesize[1] - h - 36  # 70 puede ser un margen superior que desees mantener
        first_page_table.drawOn(c, 20, high + 55)  # Posición en la primera página

        # Agregar una nueva página y dibujar las filas restantes en la segunda página
        c.showPage()
        remaining_data = data[rows_per_page + 1:]
        remaining_table = Table(remaining_data, colWidths=[1 * cm, 1.2 * cm, 10 * cm, 1.5 * cm, 1.2 * cm, 1.5 * cm,1.5 * cm, 1.5 * cm,])
        remaining_table.setStyle(table_style2)
        remaining_table.wrapOn(c, c._pagesize[0], c._pagesize[1])
        remaining_table_height = len(remaining_data) * 18
        remaining_table_y = c._pagesize[1] - 70 - remaining_table_height - 10  # Espacio para el encabezado
        remaining_table.drawOn(c, 20, remaining_table_y)  # Posición en la segunda página
        
        c.setFillColor(black)
        c.setLineWidth(.2)
        c.setFont('Helvetica',8)
        # Agregar el encabezado en la segunda página
        c.drawString(410,caja_iso + 10,'Preparado por:')
        c.drawString(410,caja_iso,'Adquisiciones')
        c.drawString(500,caja_iso + 10,'Aprobación')
        c.drawString(475,caja_iso,'Subdirección Administrativa')
        c.drawString(20,caja_iso-20,'Número de documento')
        c.drawString(30,caja_iso-30,'F-ADQ-N4-01.02')
        c.drawString(145,caja_iso-20,'Clasificación del documento')
        c.drawString(175,caja_iso-30,'Registro')
        c.drawString(255,caja_iso-20,'Nivel del documento')
        c.drawString(280,caja_iso-30, 'N5')
        c.drawString(340,caja_iso-20,'Revisión No.')
        c.drawString(352,caja_iso-30,'001')
        c.drawString(410,caja_iso-20,'Fecha de Emisión')
        c.drawString(425,caja_iso-30,'')
        c.drawString(500,caja_iso-20,'Fecha de Modificación')
        c.drawString(525,caja_iso-30,'')

        caja_proveedor = caja_iso - 65
        c.setFont('Helvetica', 12)
        c.setFillColor(prussian_blue)
        c.rect(150,750,250,30, fill=True, stroke=False) #Barra azul superior Orden de Compra
        c.setFillColor(colors.white)
        c.setFont('Helvetica-Bold', 14)
        c.drawCentredString(280, 760, 'Orden de compra')
        c.drawInlineImage('static/images/logo vordtec_documento.png',40,755, 1.5 * cm, 0.75 * cm) #Imagen vortec
    
    high = 700
    data_c.append(['''Partida''','''Cantidad''','''Código''','''Producto/Servicio''','''Criticidad''','''Descripción General''','''Especificaciones Técnicas''','''Criterios de aceptación'''])
    item = 0
    for producto in productos:
        item = item + 1
        try:
            producto_calidad = str(producto.producto.articulos.producto.producto.producto_calidad.requisitos)
        except AttributeError:
            producto_calidad = None
        data_c.append([
            item,
            producto.cantidad, 
            producto.producto.producto.articulos.producto.producto.codigo,
            'Servicio' if producto.producto.producto.articulos.producto.producto.servicio else 'Producto',
            producto.producto.producto.articulos.producto.producto.critico.nombre if producto.producto.producto.articulos.producto.producto.critico else 'ND',
            producto.producto.producto.articulos.producto.producto.nombre,
            producto.producto.producto.articulos.producto.producto.especs,
            producto_calidad,
            #producto.producto.articulos.producto.producto.producto_calidad.requisitos,
        ])
        high = high - 18
    table = Table(data_c, colWidths=[1.2 * cm, 1.5 * cm, 1.2 * cm, 2.2 * cm, 1.5 * cm, 4.2 * cm, 4.2 * cm, 4.2 * cm,])
    table_style_criticos = TableStyle([ #estilos de la tabla
        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.white),
        ('BOX',(0,0),(-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        #ENCABEZADO
        ('TEXTCOLOR',(0,0),(-1,0), white),
        ('FONTSIZE',(0,0),(-1,0), 7),
        ('BACKGROUND',(0,0),(-1,0), prussian_blue),
        #CUERPO
        ('TEXTCOLOR',(0,1),(-1,-1), colors.black),
        ('FONTSIZE',(0,1),(-1,-1), 6),
        ])
    table.setStyle(table_style_criticos)

    c.showPage()
    table.wrapOn(c, width, height)
    table.drawOn(c, 20, high) 
    c.setFillColor(black)
    c.setLineWidth(.2)
    c.setFont('Helvetica',8)
    c.drawString(410,caja_iso + 10,'Preparado por:')
    c.drawString(410,caja_iso,'Adquisiciones')
    c.drawString(500,caja_iso + 10,'Aprobación')
    c.drawString(475,caja_iso,'Subdirección Administrativa')
    c.drawString(20,caja_iso-20,'Número de documento')
    c.drawString(30,caja_iso-30,'F-ADQ-N4-01.02')
    c.drawString(145,caja_iso-20,'Clasificación del documento')
    c.drawString(175,caja_iso-30,'Registro')
    c.drawString(255,caja_iso-20,'Nivel del documento')
    c.drawString(280,caja_iso-30, 'N5')
    c.drawString(340,caja_iso-20,'Revisión No.')
    c.drawString(352,caja_iso-30,'001')
    c.drawString(410,caja_iso-20,'Fecha de Emisión')
    c.drawString(425,caja_iso-30,'')
    c.drawString(500,caja_iso-20,'Fecha de Modificación')
    c.drawString(525,caja_iso-30,'')

    caja_proveedor = caja_iso - 65
    c.setFont('Helvetica', 12)
    c.setFillColor(prussian_blue)
    c.rect(150,750,250,30, fill=True, stroke=False) #Barra azul superior Orden de Compra
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(280, 760, 'Orden de compra')
    c.drawInlineImage('static/images/logo vordtec_documento.png',40,755, 1.5 * cm, 0.75 * cm) #Imagen vortec
    c.showPage()
    
    c.save()
    buf.seek(0)
    return buf


def convert_excel_matriz_compras(compras):
    response= HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename= Matriz_compras_' + str(dt.date.today())+'.xlsx'
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
    percent_style = NamedStyle(name='percent_style', number_format='0.00%')
    percent_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(percent_style)

    columns = ['Compra','Requisición','Solicitud','Solicitante','Proyecto','Subproyecto','Área','Creado','Req. Autorizada','Proveedor',
               'Crédito/Contado','Costo','Monto_Pagado','Status Pago','Status Autorización','Días de entrega','Moneda',
               'Tipo de cambio','Entrada','Fecha Entrada','Fecha Inicio','Diferencia de Fechas','Status Entrega','No Conformidades','Total en pesos']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        ws.column_dimensions[get_column_letter(col_num + 1)].width = 16
        if col_num == 5:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 25

    columna_max = len(columns)+2

    # Agregar los mensajes
    ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por Savia Vordtec. UH}').style = messages_style
    ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Vordcab S.A. de C.V.}').style = messages_style
    ws.column_dimensions[get_column_letter(columna_max)].width = 30
    ws.column_dimensions[get_column_letter(columna_max + 1)].width = 30

    # Agregar los encabezados de las nuevas columnas debajo de los mensajes
    ws.cell(row=3, column = columna_max, value="Total de OC's").style = head_style
    ws.cell(row=4, column = columna_max, value="OC dentro de tiempo").style = head_style
    ws.cell(row=5, column = columna_max, value="% de cumplimiento").style = head_style
    ws.cell(row=6, column = columna_max, value="Monto total de OC's").style = head_style

    # Asumiendo que las filas de datos comienzan en la fila 2 y terminan en row_num
    ws.cell(row=3, column=columna_max + 1, value=f"=COUNTA(A:A)-1").style = body_style
    ws.cell(row=4, column=columna_max + 1, value=f"=COUNTIF({get_column_letter(len(columns)-1)}:{get_column_letter(len(columns)-1)}, \"<=3\")").style = body_style
    ws.cell(row=5, column=columna_max + 1, value=f"={get_column_letter(columna_max+1)}4/{get_column_letter(columna_max+1)}3").style = percent_style
    ws.cell(row=6, column=columna_max + 1, value=f"=SUM({get_column_letter(len(columns))}:{get_column_letter(len(columns))})").style = money_resumen_style

    #KPIS
    ws.cell(column = columna_max, row = 8, value='7.1 Porcentaje de órdenes de compra entregadas a tiempo').style = messages_style
    ws.cell(row=9, column = columna_max, value="Total de OC's con fecha Inicio").style = head_style
    ws.cell(row=10, column = columna_max, value="OC dentro de tiempo de entrega").style = head_style
    ws.cell(row=11, column = columna_max, value="% de cumplimiento").style = head_style

     # Asumiendo que las filas de datos comienzan en la fila 2 y terminan en row_num
    ws.cell(row=9, column=columna_max + 1, value=f"=COUNTIFS(U:U, \"<>No Existe\", U:U, \"<>\")").style = body_style
    ws.cell(row=10, column=columna_max + 1, value=f"=COUNTIF(W:W, \"En tiempo\")").style = body_style
    ws.cell(row=11, column=columna_max + 1, value=f"={get_column_letter(columna_max+1)}10/{get_column_letter(columna_max+1)}9").style = percent_style

    ws.cell(column = columna_max, row = 13, value='7.2.Porcentaje de productos o servicios recibidos sin no conformidades').style = messages_style
    ws.cell(row=14, column = columna_max, value="Total de OC's recibidas").style = head_style
    ws.cell(row=15, column = columna_max, value="Total de no conformidades").style = head_style
    ws.cell(row=16, column = columna_max, value="% de cumplimiento").style = head_style


    ws.cell(row=14, column=columna_max + 1, value=f"=COUNTIF(S:S, \"Entregado\")").style = body_style
    ws.cell(row=15, column=columna_max + 1, value=f"=COUNTIFS(X:X, \"<>No Existe\", X:X, \">0\")").style = body_style
    ws.cell(row=16, column=columna_max + 1, value=f"={get_column_letter(columna_max+1)}15/{get_column_letter(columna_max+1)}14").style = percent_style

    rows = []
    for compra in compras:
        # Obtén todos los pagos relacionados con esta compra
        pagos = Pago.objects.filter(oc=compra)
       
        # Calcula el tipo de cambio promedio de estos pagos
        tipo_de_cambio_promedio_pagos = pagos.aggregate(Avg('tipo_de_cambio'))['tipo_de_cambio__avg']

        # Usar el tipo de cambio de los pagos, si existe. De lo contrario, usar el tipo de cambio de la compra
        tipo_de_cambio = tipo_de_cambio_promedio_pagos or compra.tipo_de_cambio
        autorizado_text = 'Autorizado' if compra.autorizado2 else 'No Autorizado' if compra.autorizado2 == False or compra.autorizado1 == False else 'Pendiente Autorización'
        pagado_text = 'Pagada' if compra.pagada else 'No Pagada'
        entrada_text = 'Entregado' if compra.entrada_completa else 'No Entregado'
        
        if compra.entrada_completa:  # Verificamos si entrada es True para esta compra
            entradas = Entrada.objects.filter(oc=compra)
            ultima_entrada = entradas.order_by('-entrada_date').first()
            if ultima_entrada:  # Verificamos si existe al menos una entrada
                fecha_ultima_entrada = ultima_entrada.entrada_date
                # Contabilizar no_conformidades ligadas a las entradas de esta compra
                no_conformidades_count = No_Conformidad.objects.filter(oc=compra).count()
            else:
                # No hay entradas para esta compra
                fecha_ultima_entrada = "No Existe"
                no_conformidades_count = "No Existe"
        else:
        # El atributo 'entrada' en Compra no es True
            fecha_ultima_entrada = "No existe"
            no_conformidades_count = "No Existe"
        
        if compra.pagada:
            ultimo_pago = pagos.order_by('-pagado_date').first()
        else:
            ultimo_pago = "No Existe"
        
        if compra.cond_de_pago.nombre == "CONTADO" and ultimo_pago != "No Existe":
            fecha_inicio = ultimo_pago.pagado_date
        elif compra.cond_de_pago.nombre == "CREDITO":
            fecha_inicio = compra.autorizado_date2
        else:
            fecha_inicio = "No Existe"

        if fecha_ultima_entrada != "No existe" and fecha_inicio != "No Existe":
            diferencia_fechas = (fecha_ultima_entrada - fecha_inicio).days
        elif fecha_inicio != "No Existe" and fecha_inicio is not None:
            diferencia_fechas = (date.today() - fecha_inicio).days 
        else:
            diferencia_fechas = 0

        if fecha_inicio == "No Existe":
            cumplimiento_entrada = "No Evaluable"
        elif compra.dias_de_entrega >= diferencia_fechas:
            cumplimiento_entrada = "En tiempo"
        else:
            cumplimiento_entrada = "Fuera de tiempo"


        row = [
        compra.id,
        compra.req.folio,
        compra.req.orden.folio,
        compra.req.orden.proyecto.nombre,
        compra.req.orden.subproyecto.nombre,
        compra.req.orden.area.nombre,
        f"{compra.req.orden.staff.staff.first_name} {compra.req.orden.staff.staff.last_name}",
        compra.created_at,
        compra.req.approved_at,
        compra.proveedor.nombre.razon_social,
        compra.cond_de_pago.nombre,
        compra.costo_oc,
        compra.monto_pagado,
        pagado_text,
        autorizado_text,
        compra.dias_de_entrega,
        compra.moneda.nombre,
        tipo_de_cambio,
        entrada_text,
        fecha_ultima_entrada,
        fecha_inicio,
        diferencia_fechas,
        cumplimiento_entrada,
        no_conformidades_count
    ]
        if row[16] == "DOLARES":
            if row[17] is None or row[17] < 15:
                row[17] = 17  # o compra.pago_oc.tipo_de_cambio si así es como obtienes el valor correcto de tipo_de_cambio
        elif row[17] is None:  # por si acaso, aún manejar el caso donde 'tipo_de_cambio' es None
            row[17] = ""

        rows.append(row)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            (ws.cell(row = row_num, column = col_num+1, value=str(row[col_num]))).style = body_style
            if col_num == 8 or col_num == 7 or col_num == 19 or col_num ==20:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = date_style
            if col_num == 10 or col_num == 11 or col_num == 12 or col_num == 16:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = money_style
        # Agregamos la fórmula DATEDIF. Asumiendo que las columnas 'Creado' y 'Req. Autorizada'
        # están en las posiciones 8 y 9 respectivamente (empezando desde 0), las posiciones en Excel serán 9 y 10 (empezando desde 1).
        #ws.cell(row=row_num, column=len(columns)-1, value=f"=NETWORKDAYS(I{row_num}, H{row_num})").style = body_style
        # Agregar la fórmula de "Total en pesos"
        ws.cell(row=row_num, column = len(columns), value=f"=IF(ISBLANK(R{row_num}), L{row_num}, L{row_num}*R{row_num})").style = money_style
    
    
    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)

def convert_excel_solicitud_matriz_productos(productos):
    response= HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename = OC_por_producto_' + str(dt.date.today())+'.xlsx'
    wb = Workbook()
    ws = wb.create_sheet(title='Compras_Producto')
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
    number_style = NamedStyle(name='number_style', number_format='#,##0.00')
    number_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(number_style)
    money_style = NamedStyle(name='money_style', number_format='$ #,##0.00')
    money_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(money_style)
    money_resumen_style = NamedStyle(name='money_resumen_style', number_format='$ #,##0.00')
    money_resumen_style.font = Font(name ='Calibri', size = 14, bold = True)
    wb.add_named_style(money_resumen_style)

    columns = ['OC','RQ','Sol','Solicitante','Proyecto','Subproyecto','Fecha','Proveedor','Estatus Proveedor','Área','Cantidad','Código', 'Producto','P.U.','Moneda','Tipo de Cambio','Subtotal','IVA','Total','Estatus','Pagada']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        ws.column_dimensions[get_column_letter(col_num + 1)].width = 16
        if col_num == 4 or col_num == 7:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 25
        if col_num == 9:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 30



    columna_max = len(columns)+2

    (ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por SAVIA Vordtec. UH}')).style = messages_style
    (ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Vordcab S.A. de C.V.}')).style = messages_style
    ws.column_dimensions[get_column_letter(columna_max)].width = 20

    rows = []

    for producto in productos:
        # Extract the needed attributes
        compra_id = producto.oc.id
        req_folio = producto.oc.req.folio
        orden_folio = producto.oc.req.orden.folio
        staff_name = f"{producto.oc.req.orden.staff.staff.first_name} {producto.oc.req.orden.staff.staff.last_name}"
        proyecto_nombre = producto.oc.req.orden.proyecto.nombre
        subproyecto_nombre = producto.oc.req.orden.subproyecto.nombre
        created_at = producto.oc.created_at
        proveedor_nombre = producto.oc.proveedor.nombre.razon_social
        status_proveedor = producto.oc.proveedor.estatus.nombre 
        area_nombre = producto.oc.req.orden.area.nombre
        cantidad = producto.cantidad
        codigo = producto.producto.producto.articulos.producto.producto.codigo
        producto_nombre = producto.producto.producto.articulos.producto.producto.nombre
        precio_unitario = producto.precio_unitario
        moneda_nombre = producto.oc.moneda.nombre
        if producto.oc.autorizado2:
            estatus = 'Autorizada'
        elif producto.oc.autorizado1 == False or producto.oc.autorizado2 == False:
            estatus = 'Cancelada'  
        else:
            estatus = 'No autorizada aún'
        pagada = 'SI' if producto.oc.pagada == True else "NO"

        # Calculate total, subtotal, and IVA using attributes from producto
        subtotal = producto.subtotal_parcial
        iva = producto.iva_parcial
        total = producto.total
       

        # Handling the currency conversion logic
        pagos = Pago.objects.filter(oc_id=compra_id)
        tipo_de_cambio_promedio_pagos = pagos.aggregate(Avg('tipo_de_cambio'))['tipo_de_cambio__avg']
        tipo_de_cambio = tipo_de_cambio_promedio_pagos or producto.oc.tipo_de_cambio

        if moneda_nombre == "DOLARES" and tipo_de_cambio:
            total = total * tipo_de_cambio

        # Constructing the row
        row = [
            compra_id,
            req_folio, 
            orden_folio, 
            staff_name, 
            proyecto_nombre, 
            subproyecto_nombre, 
            created_at,
            proveedor_nombre,
            status_proveedor,
            area_nombre,
            cantidad, 
            codigo, 
            producto_nombre, 
            precio_unitario,
            moneda_nombre, 
            tipo_de_cambio, 
            subtotal, 
            iva, 
            total, 
            estatus,
            pagada
        ]
        rows.append(row)

    # Building the Excel sheet with rows
    for row in rows:
        row_num += 1
        for col_num, cell_value in enumerate(row):
            ws.cell(row=row_num, column=col_num + 1, value=str(cell_value)).style = body_style
            if col_num == 5:
                ws.cell(row=row_num, column=col_num + 1, value=cell_value).style = body_style
            if col_num == 9:
                ws.cell(row=row_num, column=col_num + 1, value=cell_value).style = number_style
            if col_num in [13, 16, 17, 18]:
                ws.cell(row=row_num, column=col_num + 1, value=cell_value).style = money_style

    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)

def convert_excel_productos_requisitados(articulos):
    response= HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename = Requisiciones_por_producto_' + str(dt.date.today())+'.xlsx'
    wb = Workbook()
    ws = wb.create_sheet(title='Productos_Requisitados')
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
    number_style = NamedStyle(name='number_style', number_format='#,##0.00')
    number_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(number_style)
    money_style = NamedStyle(name='money_style', number_format='$ #,##0.00')
    money_style.font = Font(name ='Calibri', size = 10)
    wb.add_named_style(money_style)
    money_resumen_style = NamedStyle(name='money_resumen_style', number_format='$ #,##0.00')
    money_resumen_style.font = Font(name ='Calibri', size = 14, bold = True)
    wb.add_named_style(money_resumen_style)

    columns = ['RQ','Sol','Solicitante','Proyecto','Subproyecto','Fecha','Área','Cantidad','Código', 'Producto']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        ws.column_dimensions[get_column_letter(col_num + 1)].width = 16
        if col_num == 4 or col_num == 7:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 25
        if col_num == 9:
            ws.column_dimensions[get_column_letter(col_num + 1)].width = 30



    columna_max = len(columns)+2

    (ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por Savia Vordtec. UH}')).style = messages_style
    (ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Grupo Vordcab S.A. de C.V.}')).style = messages_style
    ws.column_dimensions[get_column_letter(columna_max)].width = 20

    rows = []

    for producto in articulos:
        # Extract the needed attributes
        req_folio = producto.req.folio
        orden_folio = producto.req.orden.folio
        staff_name = f"{producto.req.orden.staff.staff.first_name} {producto.req.orden.staff.staff.last_name}"
        proyecto_nombre = producto.req.orden.proyecto.nombre
        subproyecto_nombre = producto.req.orden.subproyecto.nombre
        created_at = producto.req.created_at.replace(tzinfo=None)
        area_nombre = producto.req.orden.area.nombre
        cantidad = producto.cantidad
        codigo =producto.producto.articulos.producto.producto.codigo
        producto_nombre = producto.producto.articulos.producto.producto.nombre
      
        # Constructing the row
        row = [
            req_folio, 
            orden_folio, 
            staff_name, 
            proyecto_nombre, 
            subproyecto_nombre, 
            created_at,
            area_nombre,
            cantidad, 
            codigo, 
            producto_nombre, 
        ]
        rows.append(row)

    # Building the Excel sheet with rows
    for row in rows:
        row_num += 1
        for col_num, cell_value in enumerate(row):
            ws.cell(row=row_num, column=col_num + 1, value=str(cell_value)).style = body_style
            if col_num == 5:
                ws.cell(row=row_num, column=col_num + 1, value=cell_value).style = body_style
            if col_num == 9:
                ws.cell(row=row_num, column=col_num + 1, value=cell_value).style = number_style
           

    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)
