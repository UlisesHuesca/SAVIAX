from django.shortcuts import render, redirect
from dashboard.models import Inventario, Order, ArticulosOrdenados, ArticulosparaSurtir
from requisiciones.models import Requis, ArticulosRequisitados
from user.models import Profile
from .filters import CompraFilter
from .models import ArticuloComprado, Compra, Proveedor_completo, Cond_credito, Uso_cfdi, Moneda
from .forms import CompraForm, ArticuloCompradoForm, ArticulosRequisitadosForm, CompraFactForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import json
from django.contrib import messages
from datetime import date, datetime
from djmoney.money import Money
from num2words import num2words
#PDF generator
import io
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import Color, black, blue, red, white
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
import urllib.request, urllib.parse, urllib.error
from django.core.mail import EmailMessage
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
    requis = Requis.objects.filter(autorizar=True, colocada=False)

    tag = dof()

    context= {
        'requis':requis,
        'tags':tag,
        }

    return render(request, 'compras/requisiciones_autorizadas.html',context)

def dof():
#Trying to fetch DOF
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
        cantidad_total = productos.cantidad_comprada + int(cantidad)
        if cantidad_total > productos.cantidad:
            messages.error(request,f'La cantidad que se quiere comprar sobrepasa la cantidad requisitada {cantidad_total} mayor que {productos.cantidad}')
        else:
            comp_item, created = ArticuloComprado.objects.get_or_create(oc=oc, producto=productos)
            productos.cantidad_comprada = productos.cantidad_comprada + int(cantidad)
            messages.success(request,f'Estos son los productos comprados ahora {productos.cantidad_comprada}')
            if productos.cantidad_comprada == productos.cantidad:
                productos.art_surtido = True
            if comp_item.cantidad == None:
                comp_item.cantidad = 0
            comp_item.cantidad = comp_item.cantidad + int(cantidad)
            comp_item.precio_unitario = Money(precio,'MXN')
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

    return JsonResponse('Item updated, action executed: '+data["action"], safe=False)

def oc_modal(request, pk):
    productos = ArticulosRequisitados.objects.filter(req = pk, sel_comp = False)
    req = Requis.objects.get(id = pk)
    usuario = Profile.objects.get(id=request.user.id)
    compras = Compra.objects.all()
    oc, created = Compra.objects.get_or_create(complete = False, req = req, creada_por = usuario)
    consecutivo = compras.count() + 1
    productos_comp = ArticuloComprado.objects.filter(oc=oc)
    form_product = ArticuloCompradoForm()
    form = CompraForm(instance=oc)
    tag = dof()
    subtotal = 0
    iva = 0
    total = 0
    dif_cant = 0
    for item in productos_comp:
        subtotal = subtotal + item.cantidad * item.precio_unitario
        if item.producto.producto.articulos.producto.producto.iva == True:
            iva = iva + subtotal * 0.16
        total = subtotal + iva

    if request.method == 'POST' and  "crear" in request.POST:
        form = CompraForm(request.POST, instance=oc)
        costo_oc = 0
        costo_iva = 0
        articulos = ArticuloComprado.objects.filter(oc=oc)
        requisitados = ArticulosRequisitados.objects.filter(req = pk)
        cuenta_art_comprados = requisitados.filter(art_surtido = True).count()
        cuenta_art_totales = requisitados.count()
        if cuenta_art_totales == cuenta_art_comprados:
            req.colocada = True
        for articulo in articulos:
            costo_oc = costo_oc + articulo.precio_unitario * articulo.cantidad
            if articulo.producto.producto.articulos.producto.producto.iva == True:
                costo_iva = costo_iva = costo_oc * 0.16
        for producto in requisitados:
            dif_cant = dif_cant + producto.cantidad - producto.cantidad_comprada
            if producto.art_surtido == False:
                producto.sel_comp = False
                producto.save()
        oc.complete = True
        if oc.tipo_de_cambio != None and oc.tipo_de_cambio > 0:
            oc.costo_iva = Money(costo_iva,'USD')
            oc.costo_oc = Money(costo_oc + costo_iva,'USD')
        else:
            oc.costo_iva = costo_iva
            oc.costo_oc = costo_oc + costo_iva
        if form.is_valid():
            abrev= usuario.distrito.abreviado
            oc.folio = str(abrev) + str(consecutivo).zfill(4)
            form.save()
            oc.save()
            req.save()
            messages.success(request,f'{usuario.staff.first_name}, Haz generado la OC {oc.folio} correctamente')
            return redirect('requisicion-autorizada')

    context= {
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
        }
    return render(request, 'compras/oc.html',context)


@login_required(login_url='user-login')
def matriz_oc(request):
    compras = Compra.objects.filter(complete=True)
    myfilter = CompraFilter(request.GET, queryset=compras)
    compras = myfilter.qs

    #if request.method == 'POST' and 'btn_OC' in request.POST:

        #return oc_pdf(request, pk)

    context= {
        'compras':compras,
        'myfilter':myfilter,
        }

    return render(request, 'compras/matriz_compras.html',context)

@login_required(login_url='user-login')
def upload_facturas(request, pk):
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
    compras = Compra.objects.filter(complete=True, autorizado1= None).order_by('-folio')



    context= {
        'compras':compras,
        }

    return render(request, 'compras/autorizacion_oc1.html',context)

def cancelar_oc1(request, pk):
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc = pk)

    if compra.costo_fletes == None:
        costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    if compra.tipo_de_cambio:
        costo_oc = Money((compra.costo_oc.amount * compra.tipo_de_cambio.amount), 'MXN')
        if compra.costo_fletes:
            costo_fletes = Money(compra.costo_fletes * compra.tipo_de_cambio, 'MXN')
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes
    costo_total = costo_fletes + costo_oc
    resta = compra.req.orden.subproyecto.presupuesto - costo_total - compra.req.orden.subproyecto.gastado
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)

    if request.method == 'POST':
        compra.autorizada1_por = perfil
        compra.autorizado1 = False
        compra.autorizado_date1 = date.today()
        compra.autorizado_hora1 = datetime.now().time()
        compra.save()
        messages.error(request,f'Has cancelado la compra con FOLIO: {compra.folio}')
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
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc = pk)

    if compra.costo_fletes == None:
        costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    if compra.tipo_de_cambio:
        costo_oc = Money((compra.costo_oc.amount * compra.tipo_de_cambio.amount), 'MXN')
        if compra.costo_fletes:
            costo_fletes = Money(compra.costo_fletes * compra.tipo_de_cambio, 'MXN')
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes
    costo_total = costo_fletes + costo_oc
    resta = compra.req.orden.subproyecto.presupuesto - costo_total - compra.req.orden.subproyecto.gastado
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)


    if request.method == 'POST':
        compra.autorizada2_por = perfil
        compra.autorizado2 = False
        compra.autorizado_date2 = date.today()
        compra.autorizado_hora2 = datetime.now().time()
        compra.save()
        messages.error(request,f'Has cancelado la compra con FOLIO: {compra.folio}')
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
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc = pk)
    #Traigo la requisición para poderla activar de nuevo
    requi = Requis.objects.get(id=compra.req.id)

    if compra.costo_fletes == None:
        costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    if compra.tipo_de_cambio:
        costo_oc = Money((compra.costo_oc.amount * compra.tipo_de_cambio.amount), 'MXN')
        if compra.costo_fletes:
            costo_fletes = Money(compra.costo_fletes * compra.tipo_de_cambio, 'MXN')
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes
    costo_total = costo_fletes + costo_oc
    resta = compra.req.orden.subproyecto.presupuesto - costo_total - compra.req.orden.subproyecto.gastado
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)


    if request.method == 'POST':
        compra.autorizada2_por = perfil
        compra.autorizado2 = False
        compra.autorizado_date2 = date.today()
        compra.autorizado_hora2 = datetime.now().time()
        #Esta línea es la que activa a la requi
        requi.colocada = False
        for producto in productos:
            #La cantidad de compra pendiente tiene que sumar los artículos procedente de esta cancelación es decir,
            if producto.cantidad_pendiente == None:
                producto.cantidad_pendiente = 0
            producto.cantidad_pendiente = producto.cantidad_pendiente + producto.cantidad
            #Ahora quiero devolver las cantidades que se pueden comprar, por ello mando a llamar a los productos requisitados
            producto_requisitado = ArticulosRequisitados.objects.get(req = requi, producto = producto.producto.producto)
            if producto_requisitado != None:
                #ahora a devolverle las cantidades compradas
                #con esta línea devuelvo las cantidades que se compraron y ahora están canceladas
                producto_requisitado.cantidad_comprada = producto_requisitado.cantidad_comprada - producto.cantidad
                #con esto reactivo el producto
                producto_requisitado.art_surtido = False
                producto_requisitado.sel_comp = False
        compra.save()
        producto.save()
        producto_requisitado.save()
        requi.save()
        messages.error(request,f'Has regresado la compra con FOLIO: {compra.folio} y ahora podrás encontrar esos productos en la requisición {requi.folio}')
        return redirect('requisicion-autorizada')

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

    return render(request,'compras/back_oc.html', context)




def autorizar_oc1(request, pk):
    usuario = Profile.objects.get(id=request.user.id)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc=pk)

    if compra.costo_fletes == None:
        costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    if compra.tipo_de_cambio:
        costo_oc = Money((compra.costo_oc.amount * compra.tipo_de_cambio.amount), 'MXN')
        if compra.costo_fletes:
            costo_fletes = Money(compra.costo_fletes * compra.tipo_de_cambio, 'MXN')
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes
    costo_total = costo_fletes + costo_oc
    resta = compra.req.orden.subproyecto.presupuesto - costo_oc - costo_fletes - compra.req.orden.subproyecto.gastado
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)


    if request.method == 'POST':
        compra.autorizado1 = True
        compra.oc_autorizada_por = usuario
        compra.autorizado_date1 = date.today()
        compra.autorizado_hora1 = datetime.now().time()
        compra.save()
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

    compras = Compra.objects.filter(complete = True, autorizado1 = True, autorizado2= None).order_by('-folio')

    context= {
        'compras':compras,
        }

    return render(request, 'compras/autorizacion_oc2.html',context)


def autorizar_oc2(request, pk):
    usuario = Profile.objects.get(id=request.user.id)
    compra = Compra.objects.get(id = pk)
    productos = ArticuloComprado.objects.filter(oc=pk)

    if compra.costo_fletes == None:
        costo_fletes = 0
    #Si hay tipo de cambio es porque la compra fue en dólares entonces multiplico por tipo de cambio la cantidad
    #Escenario con dólares
    if compra.tipo_de_cambio:
        costo_oc = Money((compra.costo_oc.amount * compra.tipo_de_cambio.amount), 'MXN')
        if compra.costo_fletes:
            costo_fletes = Money(compra.costo_fletes * compra.tipo_de_cambio, 'MXN')
    #Escenario con pesos
    else:
        costo_oc = compra.costo_oc
        if compra.costo_fletes:
            costo_fletes = compra.costo_fletes
    costo_total = costo_fletes + costo_oc
    resta = compra.req.orden.subproyecto.presupuesto - costo_oc - costo_fletes - compra.req.orden.subproyecto.gastado
    porcentaje = "{0:.2f}%".format((costo_oc/compra.req.orden.subproyecto.presupuesto)*100)

    if request.method == 'POST':
        compra.autorizado2 = True
        compra.oc_autorizada_por2 = usuario
        compra.autorizado_date2 = date.today()
        compra.autorizado_time2 = datetime.now().time()
        compra.save()
        if compra.cond_de_pago.nombre == "Crédito":
            archivo_oc = attach_oc_pdf(request, compra.id)
            email = EmailMessage(
                f'Compra Autorizada {compra.folio}',
                f'Estimado proveedor,\n Estás recibiendo este correo porque has sido seleccionado para surtirnos la compra con folio: {compra.folio}.\n Este mensaje ha sido automáticamente generado por SAVIA X',
                'saviax.vordcab@gmail.com',
                [compra.proveedor.email],
                )
            email.attach(f'OC_folio:{compra.folio}.pdf',archivo_oc,'application/pdf')
            email.send()
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

def render_oc_pdf(request, pk):
    #Configuration of the PDF object
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    #Here ends conf.
    compra = Compra.objects.get(id=pk)
    productos = ArticuloComprado.objects.filter(oc=pk)



    #Azul Vordcab
    prussian_blue = Color(0.0859375,0.1953125,0.30859375)
    rojo = Color(0.59375, 0.05859375, 0.05859375)
    #Encabezado
    c.setFillColor(black)
    c.setLineWidth(.2)
    c.setFont('Helvetica',12)
    c.drawString(460,735,'Folio: ')
    c.drawString(270,735,'Fecha:')

    c.setFillColor(prussian_blue)
    # REC (Dist del eje Y, Dist del eje X, LARGO DEL RECT, ANCHO DEL RECT)
    c.rect(200,750,300,20, fill=True, stroke=False) #Barra azul superior Orden de Compra
    c.rect(20,708,565,20, fill=True, stroke=False) #Barra azul superior Proveedor | Detalle
    c.rect(20,520,565,2, fill=True, stroke=False) #Linea posterior horizontal
    c.setFillColor(white)
    c.setLineWidth(.2)
    c.setFont('Helvetica-Bold',14)
    c.drawCentredString(360,755,'Orden de compra')
    c.setLineWidth(.3) #Grosor
    c.line(20,727.5,20,520) #Eje Y donde empieza, Eje X donde empieza, donde termina eje y,donde termina eje x (LINEA 1 contorno)
    c.line(585,727.5,585,520) #Linea 2 contorno
    c.drawInlineImage('static/images/Logo-Vordtec.png',45,730, 3 * cm, 1.5 * cm) #Imagen vortec


    c.setFillColor(white)
    c.setFont('Helvetica-Bold',11)
    c.drawString(120,715,'Proveedor')
    c.drawString(450,715, 'Detalle')
    inicio_central = 370
    c.line(inicio_central,707,inicio_central,520) #Linea Central de caja Proveedor | Detalle
    c.setFillColor(black)
    c.setFont('Helvetica',9)
    c.drawString(30,700,'Proveedor:')
    c.drawString(30,680,'RFC:')
    c.drawString(30,660,'Solicitó:')
    #c.drawString(30,645,'Fecha:')
    c.drawString(30,640,'Banco:')
    c.drawString(30,620,'Cuenta:')
    c.drawString(30,600,'Clabe:')
    c.drawString(30,580,'Uso del CFDI:')
    c.drawString(30,560,'Proveedor Calif:')

    c.drawString(inicio_central + 10,680,'No. Requisición:')
    c.drawString(inicio_central + 10,660,'Condiciones pago:')
    c.drawString(inicio_central + 10,640,'Lugar de entrega:')
    c.drawString(inicio_central + 10,620,'Anticipo:')
    c.drawString(inicio_central + 10,600,'A.F:')
    c.drawString(inicio_central + 10,580,'Enviar a:')
    if compra.req.orden.activo.eco_unidad != "NA":
        c.drawString(300,560,'A.F. Desc:')


    c.setFont('Helvetica',12) ## FECHA DE LA SOLICITUD 505,735
    c.drawString(310,735, compra.created_at.strftime("%d/%m/%Y"))
    c.setFillColor(rojo) ## NUMERO DEL FOLIO
    c.drawString(495,735, str(compra.id))
    c.setFillColor(black)
    c.setFont('Helvetica',9)
    c.drawString(80,700, compra.proveedor.nombre.nombre)
    c.drawString(80,680, compra.proveedor.nombre.rfc)
    c.drawString(80,660, compra.req.orden.staff.staff.first_name +' '+ compra.req.orden.staff.staff.last_name)
    c.drawString(80,640, compra.proveedor.banco.nombre)
    c.drawString(80,620, compra.proveedor.cuenta)
    c.drawString(80,600, compra.proveedor.clabe)
    c.drawString(120,580, compra.uso_del_cfdi.descripcion)
    c.drawString(120,560, compra.proveedor.estatus.nombre)

    c.drawString(inicio_central + 90,680, str(compra.req.id))
    if compra.cond_de_pago.nombre == "Crédito":
        c.drawString(inicio_central + 80,660, compra.cond_de_pago.nombre + '  ' + str(compra.dias_de_credito) + 'días')
    else:
        c.drawString(inicio_central + 90,660, compra.cond_de_pago.nombre )
    c.drawString(inicio_central + 90,640, 'Almacén '+ compra.req.orden.staff.distrito.nombre)
    if compra.anticipo == False:
        compra.monto_anticipo = 0
    c.drawString(inicio_central + 70,620, str(compra.monto_anticipo))
    c.drawString(inicio_central + 70,600, compra.req.orden.activo.eco_unidad)
    c.drawString(inicio_central + 70,580, compra.creada_por.staff.email)
    if compra.req.orden.activo.eco_unidad != "NA":
        c.drawString(inicio_central + 80,560, compra.req.orden.activo.tipo)


    data =[]
    high = 495
    data.append(['''Código''','''Producto''', '''Cantidad''', '''Unidad''', '''P.Unitario''', '''Importe'''])
    for producto in productos:
        data.append([producto.producto.producto.articulos.producto.producto.codigo, producto.producto.producto.articulos.producto.producto.nombre,producto.cantidad, producto.producto.producto.articulos.producto.producto.unidad, producto.precio_unitario, producto.precio_unitario * producto.cantidad])
        high = high - 18

    c.setFillColor(black)
    c.setFont('Helvetica',8)
    c.drawString(30,high-40,'FACTURAR A: ')
    c.drawString(30,high-60,'DOMICILIO ENTREGADO: ')
    c.drawString(30,high-80,'HORARIO ENTREGA: ')
    c.setFillColor(prussian_blue)
    # REC (Dist del eje Y, Dist del eje X, LARGO DEL RECT, ANCHO DEL RECT)
    c.rect(20,high-125,340,20, fill=True, stroke=False) #3ra linea azul
    c.setFillColor(black)
    c.setFont('Helvetica',7)
    c.drawString(95,high-40,'GRUPO VORDCAB, S.A. DE C.V. DOMICILIO: LAZARO CARDENAS N° 227 COL. TAMPICO C.P.89609 ALTAMIRA TAMAULIPAS RFC: GVO-020226-811')
    c.drawString(135,high-60,'RECEPCIÓN ALMACEN: LUNES A VIERNES 9:00 HRS A 12:00 HRS Y DE 14:00 A 16:00 HRS')
    c.drawString(115,high-80,'ENTREGA EN NUESTRO ALMACÉN OPERATIVO EN BLVD. PRIMEX KM 3.2 EJIDO LAGUNA DE LA PUERTA C.P. 89603')

    c.setFillColor(white)
    c.setLineWidth(.1)
    c.setFont('Helvetica-Bold',10)
    c.drawCentredString(70,high-120,'Proyecto')
    c.drawCentredString(165,high-120,'Subproyecto')
    c.drawCentredString(240,high-120,'Elaboró')
    c.drawCentredString(315,high-120,'Moneda')
    c.setFont('Helvetica',8)
    c.setFillColor(black)
    c.drawCentredString(70,high-140,compra.req.orden.proyecto.nombre)
    c.drawCentredString(165,high-140,compra.req.orden.subproyecto.nombre)
    c.drawCentredString(240,high-140,compra.creada_por.staff.first_name + ' ' +compra.creada_por.staff.last_name)
    c.drawCentredString(315,high-140,compra.moneda.nombre)


    c.setLineWidth(.3)
    c.line(370,high-95,370,high-160) #Eje Y donde empieza, Eje X donde empieza, donde termina eje y,donde termina eje x (LINEA 1 contorno)
    c.line(370,high-160,560,high-160)

    c.setFillColor(black)
    c.setFont('Helvetica-Bold',9)

    montos_align = 480
    c.drawRightString(montos_align,high-115,'Sub Total:')
    c.drawRightString(montos_align,high-125,'IVA 16%:')
    c.drawRightString(montos_align,high-135,'Importe Neto:')
    c.drawRightString(montos_align,high-145,'Costo fletes:')
    c.setFillColor(prussian_blue)
    c.drawRightString(montos_align,high-155,'Total:')
    c.setFillColor(black)
    c.drawString(35,high-200,'Opciones y condiciones:')
    c.setFont('Helvetica',8)
    letras = 350
    c.drawString(letras-90,high-175,'Total con letra:')
    c.line(135,high-240,215, high-240) #Linea de Autorizacion
    c.line(350,high-240,430, high-240)
    c.drawCentredString(175,high-250,'Autorización')
    c.drawCentredString(390,high-250,'Autorización')

    c.drawCentredString(175,high-270,'Superintendente Administrativo')
    c.drawCentredString(390,high-270,'Gerencia Zona')
    c.drawCentredString(175,high-230,'Rafael Delgado')
    c.drawCentredString(390,high-230,'Martha Mendez Fraga')

    c.setFont('Helvetica',10)
    subtotal = compra.costo_oc - compra.costo_iva
    c.drawRightString(montos_align + 90,high-115,str(subtotal))
    c.drawRightString(montos_align + 90,high-125,str(compra.costo_iva))
    c.drawRightString(montos_align + 90,high-135,str(compra.costo_oc))
    if compra.costo_fletes is None:
        compra.costo_fletes = 0
    c.drawRightString(montos_align + 90,high-145,str(compra.costo_fletes))
    c.setFillColor(prussian_blue)
    c.drawRightString(montos_align + 90,high-155,str(compra.monto_pagado ))
    c.setFont('Helvetica', 9)
    c.drawString(letras,high-175, num2words(compra.monto_pagado.amount, lang='es_CO', to='currency'))
    c.setFillColor(black)
    if compra.opciones_condiciones is not None:
        c.drawString(150,high-200,compra.opciones_condiciones)
    else:
        c.drawString(150,high-200,"NA")

    c.setFillColor(prussian_blue)
    c.rect(20,30,565,30, fill=True, stroke=False)
    c.setFillColor(white)
    #Primer renglón
    c.drawCentredString(70,48,'Clasificación:')
    c.drawCentredString(140,48,'Nivel:')
    c.drawCentredString(240,48,'Preparado por:')
    c.drawCentredString(350,48,'Aprobado:')
    c.drawCentredString(450,48,'Fecha emisión:')
    c.drawCentredString(550,48,'Rev:')
    #Segundo renglón
    c.drawCentredString(70,34,'Controlado')
    c.drawCentredString(140,34,'N5')
    c.drawCentredString(240,34,'SEOV-ALM-N4-01-01')
    c.drawCentredString(350,34,'SUB ADM')
    c.drawCentredString(450,34,'24/Oct/2018')
    c.drawCentredString(550,34,'001')

    width, height = letter
    table = Table(data, colWidths=[2.8 * cm, 6 * cm, 2.8 * cm, 2.8 * cm, 2.8 * cm, 2.8 * cm])
    table.setStyle(TableStyle([ #estilos de la tabla
        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.white),
        ('BOX',(0,0),(-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        #ENCABEZADO
        ('TEXTCOLOR',(0,0),(-1,0), white),
        ('FONTSIZE',(0,0),(-1,0), 13),
        ('BACKGROUND',(0,0),(-1,0), prussian_blue),
        #CUERPO
        ('TEXTCOLOR',(0,1),(-1,-1), colors.black),
        ('FONTSIZE',(0,1),(-1,-1), 10),
        ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 20, high)
    c.save()
    c.showPage()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='oc_'+str(compra.id) +'.pdf')

def attach_oc_pdf(request, pk):
    #Configuration of the PDF object
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    #Here ends conf.
    compra = Compra.objects.get(id=pk)
    productos = ArticuloComprado.objects.filter(oc=pk)



    #Azul Vordcab
    prussian_blue = Color(0.0859375,0.1953125,0.30859375)
    rojo = Color(0.59375, 0.05859375, 0.05859375)
    #Encabezado
    c.setFillColor(black)
    c.setLineWidth(.2)
    c.setFont('Helvetica',12)
    c.drawString(460,735,'Folio: ')
    c.drawString(270,735,'Fecha:')

    c.setFillColor(prussian_blue)
    # REC (Dist del eje Y, Dist del eje X, LARGO DEL RECT, ANCHO DEL RECT)
    c.rect(200,750,300,20, fill=True, stroke=False) #Barra azul superior Orden de Compra
    c.rect(20,708,565,20, fill=True, stroke=False) #Barra azul superior Proveedor | Detalle
    c.rect(20,520,565,2, fill=True, stroke=False) #Linea posterior horizontal
    c.setFillColor(white)
    c.setLineWidth(.2)
    c.setFont('Helvetica-Bold',14)
    c.drawCentredString(360,755,'Orden de compra')
    c.setLineWidth(.3) #Grosor
    c.line(20,727.5,20,520) #Eje Y donde empieza, Eje X donde empieza, donde termina eje y,donde termina eje x (LINEA 1 contorno)
    c.line(585,727.5,585,520) #Linea 2 contorno
    c.drawInlineImage('static/images/Logo-Vordtec.png',45,730, 3 * cm, 1.5 * cm) #Imagen vortec


    c.setFillColor(white)
    c.setFont('Helvetica-Bold',11)
    c.drawString(120,715,'Proveedor')
    c.drawString(450,715, 'Detalle')
    inicio_central = 370
    c.line(inicio_central,707,inicio_central,520) #Linea Central de caja Proveedor | Detalle
    c.setFillColor(black)
    c.setFont('Helvetica',9)
    c.drawString(30,700,'Proveedor:')
    c.drawString(30,680,'RFC:')
    c.drawString(30,660,'Solicitó:')
    #c.drawString(30,645,'Fecha:')
    c.drawString(30,640,'Banco:')
    c.drawString(30,620,'Cuenta:')
    c.drawString(30,600,'Clabe:')
    c.drawString(30,580,'Uso del CFDI:')
    c.drawString(30,560,'Proveedor Calif:')

    c.drawString(inicio_central + 10,680,'No. Requisición:')
    c.drawString(inicio_central + 10,660,'Condiciones pago:')
    c.drawString(inicio_central + 10,640,'Lugar de entrega:')
    c.drawString(inicio_central + 10,620,'Anticipo:')
    c.drawString(inicio_central + 10,600,'A.F:')
    c.drawString(inicio_central + 10,580,'Enviar a:')
    if compra.req.orden.activo.eco_unidad != "NA":
        c.drawString(300,560,'A.F. Desc:')


    c.setFont('Helvetica',12) ## FECHA DE LA SOLICITUD 505,735
    c.drawString(310,735, compra.created_at.strftime("%d/%m/%Y"))
    c.setFillColor(rojo) ## NUMERO DEL FOLIO
    c.drawString(495,735, str(compra.folio))
    c.setFillColor(black)
    c.setFont('Helvetica',9)
    c.drawString(80,700, compra.proveedor.nombre.nombre)
    c.drawString(80,680, compra.proveedor.nombre.rfc)
    c.drawString(80,660, compra.req.orden.staff.staff.first_name +' '+ compra.req.orden.staff.staff.last_name)
    c.drawString(80,640, compra.proveedor.banco.nombre)
    c.drawString(80,620, compra.proveedor.cuenta)
    c.drawString(80,600, compra.proveedor.clabe)
    c.drawString(120,580, compra.uso_del_cfdi.descripcion)
    c.drawString(120,560, compra.proveedor.estatus.nombre)

    c.drawString(inicio_central + 90,680, str(compra.req.folio))
    if compra.cond_de_pago.nombre == "Crédito":
        c.drawString(inicio_central + 80,660, compra.cond_de_pago.nombre + '  ' + str(compra.dias_de_credito) + 'días')
    else:
        c.drawString(inicio_central + 90,660, compra.cond_de_pago.nombre )
    c.drawString(inicio_central + 90,640, 'Almacén '+ compra.req.orden.staff.distrito.nombre)
    if compra.anticipo == False:
        compra.monto_anticipo = 0
    c.drawString(inicio_central + 70,620, str(compra.monto_anticipo))
    c.drawString(inicio_central + 70,600, compra.req.orden.activo.eco_unidad)
    c.drawString(inicio_central + 70,580, compra.creada_por.staff.email)
    if compra.req.orden.activo.eco_unidad != "NA":
        c.drawString(inicio_central + 80,560, compra.req.orden.activo.tipo)


    data =[]
    high = 495
    data.append(['''Código''','''Producto''', '''Cantidad''', '''Unidad''', '''P.Unitario''', '''Importe'''])
    for producto in productos:
        data.append([producto.producto.producto.articulos.producto.producto.codigo, producto.producto.producto.articulos.producto.producto.nombre,producto.cantidad, producto.producto.producto.articulos.producto.producto.unidad, producto.precio_unitario, producto.precio_unitario * producto.cantidad])
        high = high - 18

    c.setFillColor(black)
    c.setFont('Helvetica',8)
    c.drawString(30,high-40,'FACTURAR A: ')
    c.drawString(30,high-60,'DOMICILIO ENTREGADO: ')
    c.drawString(30,high-80,'HORARIO ENTREGA: ')
    c.setFillColor(prussian_blue)
    # REC (Dist del eje Y, Dist del eje X, LARGO DEL RECT, ANCHO DEL RECT)
    c.rect(20,high-125,340,20, fill=True, stroke=False) #3ra linea azul
    c.setFillColor(black)
    c.setFont('Helvetica',7)
    c.drawString(95,high-40,'VORDTEC DE MÉXICO DOMICILIO: LAZARO CARDENAS N° 227 COL. TAMPICO C.P.89609 ALTAMIRA TAMAULIPAS RFC: GVO-020226-811')
    c.drawString(135,high-60,'RECEPCIÓN ALMACEN: LUNES A VIERNES 9:00 HRS A 12:00 HRS Y DE 14:00 A 16:00 HRS')
    c.drawString(115,high-80,'ENTREGA EN NUESTRO ALMACÉN OPERATIVO EN BLVD. PRIMEX KM 3.2 EJIDO LAGUNA DE LA PUERTA C.P. 89603')

    c.setFillColor(white)
    c.setLineWidth(.1)
    c.setFont('Helvetica-Bold',10)
    c.drawCentredString(70,high-120,'Proyecto')
    c.drawCentredString(165,high-120,'Subproyecto')
    c.drawCentredString(240,high-120,'Elaboró')
    c.drawCentredString(315,high-120,'Moneda')
    c.setFont('Helvetica',8)
    c.setFillColor(black)
    c.drawCentredString(70,high-140,compra.req.orden.proyecto.nombre)
    c.drawCentredString(165,high-140,compra.req.orden.subproyecto.nombre)
    c.drawCentredString(240,high-140,compra.creada_por.staff.first_name + ' ' +compra.creada_por.staff.last_name)
    c.drawCentredString(315,high-140,compra.moneda.nombre)


    c.setLineWidth(.3)
    c.line(370,high-95,370,high-160) #Eje Y donde empieza, Eje X donde empieza, donde termina eje y,donde termina eje x (LINEA 1 contorno)
    c.line(370,high-160,560,high-160)

    c.setFillColor(black)
    c.setFont('Helvetica-Bold',9)

    montos_align = 480
    c.drawRightString(montos_align,high-115,'Sub Total:')
    c.drawRightString(montos_align,high-125,'IVA 16%:')
    c.drawRightString(montos_align,high-135,'Importe Neto:')
    c.drawRightString(montos_align,high-145,'Costo fletes:')
    c.setFillColor(prussian_blue)
    c.drawRightString(montos_align,high-155,'Total:')
    c.setFillColor(black)
    c.drawString(35,high-200,'Opciones y condiciones:')
    c.setFont('Helvetica',8)
    letras = 350
    c.drawString(letras-90,high-175,'Total con letra:')
    c.line(135,high-240,215, high-240) #Linea de Autorizacion
    c.line(350,high-240,430, high-240)
    c.drawCentredString(175,high-250,'Autorización')
    c.drawCentredString(390,high-250,'Autorización')

    c.drawCentredString(175,high-270,'Superintendente Administrativo')
    c.drawCentredString(390,high-270,'Gerencia Zona')
    c.drawCentredString(175,high-230,'Rafael Delgado')
    c.drawCentredString(390,high-230,'Martha Mendez Fraga')

    c.setFont('Helvetica',10)
    subtotal = compra.costo_oc - compra.costo_iva
    c.drawRightString(montos_align + 90,high-115,str(subtotal))
    c.drawRightString(montos_align + 90,high-125,str(compra.costo_iva))
    c.drawRightString(montos_align + 90,high-135,str(compra.costo_oc))
    if compra.costo_fletes is None:
        compra.costo_fletes = 0
    c.drawRightString(montos_align + 90,high-145,str(compra.costo_fletes))
    c.setFillColor(prussian_blue)
    c.drawRightString(montos_align + 90,high-155,str(compra.monto_pagado ))
    c.setFont('Helvetica', 9)
    c.drawString(letras,high-175, num2words(compra.monto_pagado.amount, lang='es_CO', to='currency'))
    c.setFillColor(black)
    if compra.opciones_condiciones is not None:
        c.drawString(150,high-200,compra.opciones_condiciones)
    else:
        c.drawString(150,high-200,"NA")

    c.setFillColor(prussian_blue)
    c.rect(20,30,565,30, fill=True, stroke=False)
    c.setFillColor(white)
    #Primer renglón
    c.drawCentredString(70,48,'Clasificación:')
    c.drawCentredString(140,48,'Nivel:')
    c.drawCentredString(240,48,'Preparado por:')
    c.drawCentredString(350,48,'Aprobado:')
    c.drawCentredString(450,48,'Fecha emisión:')
    c.drawCentredString(550,48,'Rev:')
    #Segundo renglón
    c.drawCentredString(70,34,'Controlado')
    c.drawCentredString(140,34,'N5')
    c.drawCentredString(240,34,'SEOV-ALM-N4-01-01')
    c.drawCentredString(350,34,'SUB ADM')
    c.drawCentredString(450,34,'24/Oct/2018')
    c.drawCentredString(550,34,'001')

    width, height = letter
    table = Table(data, colWidths=[2.8 * cm, 6 * cm, 2.8 * cm, 2.8 * cm, 2.8 * cm, 2.8 * cm])
    table.setStyle(TableStyle([ #estilos de la tabla
        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.white),
        ('BOX',(0,0),(-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        #ENCABEZADO
        ('TEXTCOLOR',(0,0),(-1,0), white),
        ('FONTSIZE',(0,0),(-1,0), 13),
        ('BACKGROUND',(0,0),(-1,0), prussian_blue),
        #CUERPO
        ('TEXTCOLOR',(0,1),(-1,-1), colors.black),
        ('FONTSIZE',(0,1),(-1,-1), 10),
        ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 20, high)
    c.save()
    c.showPage()
    buf.seek(0)
    return buf.getvalue()