3
from django.shortcuts import render, redirect
from dashboard.models import Inventario, Order, ArticulosparaSurtir, ArticulosOrdenados
from user.models import Profile
from .models import ArticulosRequisitados, Requis
from entradas.models import Entrada, EntradaArticulo
from requisiciones.models import Salidas
from django.contrib.auth.decorators import login_required
from .filters import ArticulosparaSurtirFilter, SalidasFilter, EntradasFilter
from .forms import SalidasForm, ArticulosRequisitadosForm
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Font, PatternFill
from openpyxl.utils import get_column_letter
import datetime as dt
from datetime import date, datetime
from django.db.models.functions import Concat
from django.db.models import Value, Sum
from django.contrib import messages
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
from django.db.models import Q
#import json

# Create your views here.
@login_required(login_url='user-login')
def solicitud_autorizada(request):
    #Aquí aparecen todas las ordenes, es decir sería el filtro para administrador, el objeto Q no tiene propiedad conmutativa
    #productos= ArticulosparaSurtir.objects.filter(Q(salida=False) | Q(requisitar=True), articulos__orden__autorizar = True )
    productos= ArticulosparaSurtir.objects.filter(salida=False, articulos__orden__autorizar = True, articulos__orden__requisitar = False, articulos__producto__producto__servicio = False, articulos__orden__tipo__tipo='normal').order_by('-articulos__orden__folio')
    myfilter = ArticulosparaSurtirFilter(request.GET, queryset=productos)
    productos = myfilter.qs


    #Here is where call a function to generate XLSX, using Openpyxl library
    if request.method == 'POST' and 'btnExcel' in request.POST:

        return convert_solicitud_autorizada_to_xls(productos)

    context= {
        'productos':productos,
        'myfilter':myfilter,
        }
    return render(request, 'requisiciones/solicitudes_autorizadas.html',context)

@login_required(login_url='user-login')
def salida_material(request, pk):
    usuario = Profile.objects.get(id=request.user.id)
    productos= ArticulosparaSurtir.objects.get(id = pk)
    prod_inventario = Inventario.objects.get(producto = productos.articulos.producto.producto)
    salida, created = Salidas.objects.get_or_create(almacenista=usuario, producto=productos, salida_firmada=False)
    orden = Salidas.objects.filter(producto__articulos__orden= productos.articulos.orden,
                                    producto = productos).aggregate(Sum('cantidad'))
    suma_salidas = orden['cantidad__sum']
    disponible = productos.cantidad - suma_salidas
    form = SalidasForm()

    if request.method == 'POST':
        #vato_que_recibe = Profile.objects.get(id=request.POST.get('material_recibido_por'))
        #cantidad_post = int(request.POST.get('cantidad'))
        #salida.material_recibido_por=vato_que_recibe

        form = SalidasForm(request.POST,instance = salida)
        form.save(commit=False)
        if salida.cantidad <= 0:
            messages.error(request, 'La cantidad capturada debe ser mayor que 0')
        else:
            cantidad_actual = suma_salidas + salida.cantidad
            if cantidad_actual > productos.cantidad:
                messages.error(request,f'La salida no ha sido creada, la cantidad de producto solicitada [{salida.cantidad}] es mayor que lo disponible [{disponible}]')
            if cantidad_actual == productos.cantidad:
                messages.success(request,'La salida ha sido creada y completada')
                prod_inventario.cantidad_apartada = prod_inventario.cantidad_apartada - salida.cantidad
                if form.is_valid():
                    prod_inventario._change_reason = 'Esta es una salida de material view:salida_material'
                    productos.salida= True
                    productos.save()
                    form.save()
                    prod_inventario.save()
            elif cantidad_actual < productos.cantidad:
                messages.success(request,f'Esta es una salida parcial de {salida.cantidad} pieza(s) de las {disponible} disponibles')
                prod_inventario.cantidad_apartada = prod_inventario.cantidad_apartada - salida.cantidad
                if form.is_valid():

                    form.save()
                    prod_inventario.save()
        return redirect('solicitud-autorizada')

    context= {
        'productos':productos,
        'form':form,
        'disponible':disponible,
        }

    return render(request, 'requisiciones/salida_material.html',context)




def solicitud_autorizada_firma(request):
    usuario = Profile.objects.get(id=request.user.id)
    #Aquí aparecen todas las ordenes, es decir sería el filtro para administrador
    productos= Salidas.objects.filter(producto__articulos__orden__autorizar = True, salida_firmada=False)
    myfilter = SalidasFilter(request.GET, queryset=productos)
    productos = myfilter.qs

    #Here is where XLSX is generated, using Openpyxl library | Aquí es donde se genera el XLSX
    if request.method == "POST" and 'btnExcel' in request.POST:

        return convert_solicitud_autorizada_orden_to_xls(productos)

    context= {
        'productos':productos,
        'myfilter':myfilter,
        'usuario':usuario,
        }
    return render(request, 'requisiciones/solicitudes_autorizadas_firma.html',context)



@login_required(login_url='user-login')
def salida_material_usuario(request, pk):
    producto= Salidas.objects.get(id = pk)
    producto_surtir = ArticulosparaSurtir.objects.get(articulos = producto.producto.articulos)

    if request.method == 'POST':
        producto.salida_firmada = True
        producto_surtir.salida = True
        producto_surtir.firma = True
        producto_surtir.save()
        producto.save()

        messages.success(request,f'Has realizado la salida del producto {producto.producto.articulos.producto.producto} con éxito')
        return redirect('solicitud-autorizada-firma')

    context= {
        'productos':producto,
    }

    return render(request, 'requisiciones/salida_material_usuario.html',context)

@login_required(login_url='user-login')
def solicitud_autorizada_orden(request):
    #obtengo el id de usuario, lo paso como argumento a id de profiles para obtener el objeto profile que coindice con ese usuario_id
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)

    #Este es un filtro por perfil supervisor o superintendente, es decir puede ver todo lo del distrito
    #productos= ArticulosparaSurtir.objects.filter(Q(salida=False) | Q(requisitar=True), articulos__orden__autorizar = True )
    ordenes = Order.objects.filter(requisitar = True, complete=True, autorizar=True, staff__distrito=perfil.distrito)

    if request.method == "POST" and 'btnExcel' in request.POST:

        return convert_solicitud_autorizada_orden_to_xls(ordenes)

    context= {
        'ordenes':ordenes,
        }

    return render(request, 'requisiciones/solicitudes_autorizadas_orden.html',context)

def detalle_orden(request, pk):
    orden = Order.objects.get(id=pk)
    productos = ArticulosOrdenados.objects.filter(orden=pk)


    context = {
        'productos': productos,
        'orden': orden,
     }
    return render(request,'requisiciones/orden_detail.html', context)

@login_required(login_url='user-login')
def requisicion_autorizacion(request):
    #obtengo el id de usuario, lo paso como argumento a id de profiles para obtener el objeto profile que coindice con ese usuario_id

    #Este es un filtro por perfil supervisor o superintendente, es decir puede ver todo lo del distrito

    #ordenes = Order.objects.filter(complete=True, autorizar=True, staff__distrito=perfil.distrito)
    requis = Requis.objects.filter(autorizar=None)


    context= {
        'requis':requis,
        }

    return render(request, 'requisiciones/requisiciones_autorizacion.html',context)

def requisicion_creada_detalle(request, pk):
    productos = ArticulosRequisitados.objects.filter(req = pk)
    requis = Requis.objects.get(id = pk)

    context = {
        'productos': productos,
        'requis': requis,
     }

    return render(request,'requisiciones/requisicion_creada_detalle.html', context)

def requisicion_detalle(request, pk):
    #Vista de creación de requisición
    productos = ArticulosparaSurtir.objects.filter(articulos__orden__id = pk, requisitar= True)
    orden = Order.objects.get(id = pk)
    usuario = Profile.objects.get(id=request.user.id)
    requi, created = Requis.objects.get_or_create(complete=False, orden=orden)
    requis = Requis.objects.filter(orden__staff__distrito = usuario.distrito)
    consecutivo = requis.count() + 1

    for producto in productos:
        requitem, created = ArticulosRequisitados.objects.get_or_create(req = requi, producto= producto, cantidad=producto.cantidad_requisitar)


    if request.method == 'POST':
        requi.complete = True
        orden.requisitar = False
        for producto in productos:
            #Vuelve false para que desaparezca de la vista pero creo que debo evaluar si es la mejor manera lo mismo para orden.requisitar = False
            producto.requisitar = False
            producto.save()
        requitem.almacenista = usuario
        requi.folio = str(usuario.distrito.abreviado)+str(consecutivo).zfill(4)
        requi.save()
        requitem.save()
        orden.save()
        messages.success(request,f'Has realizado la requisición {requi.folio} con éxito')
        return redirect('solicitud-autorizada-orden')

    context = {
        'productos': productos,
        'orden': orden,
     }

    return render(request,'requisiciones/detalle_requisitar.html', context)

def requisicion_autorizar(request, pk):
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)
    requi = Requis.objects.get(id = pk)
    productos = ArticulosRequisitados.objects.filter(req = pk)
    costo_aprox = 0
    for producto in productos:
        costo_aprox = costo_aprox + producto.cantidad * producto.producto.articulos.producto.price

    porcentaje = "{0:.2f}%".format((costo_aprox/requi.orden.subproyecto.presupuesto)*100)
    resta = requi.orden.subproyecto.presupuesto - requi.orden.subproyecto.gastado - costo_aprox

    if request.method == 'POST':
        requi.requi_autorizada_por = perfil
        requi.approved_at_time = datetime.now().time()
        requi.approved_at = date.today()
        requi.autorizar = True
        requi.save()
        messages.success(request,f'Has autorizado la requisición {requi.folio} con éxito')
        return redirect('requisicion-autorizacion')

    context = {
        'productos': productos,
        'requis': requi,
        'costo_aprox': costo_aprox,
        'porcentaje': porcentaje,
        'resta': resta,
     }

    return render(request,'requisiciones/requisiciones_autorizar.html', context)

def requisicion_cancelar(request, pk):
    usuario = request.user.id
    perfil = Profile.objects.get(id=usuario)
    requis = Requis.objects.get(id = pk)
    productos = ArticulosRequisitados.objects.filter(req = pk)

    if request.method == 'POST':
        requis.autorizada_por = perfil
        requis.autorizar = False
        requis.save()
        messages.error(request,f'Has cancelado la requisición {requis.folio}')
        return redirect('requisicion-autorizacion')

    context = {
        'productos': productos,
        'requis': requis,
     }
    return render(request,'requisiciones/requisiciones_cancelar.html', context)


def render_pdf_view(request, pk):
    #Configuration of the PDF object
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    #Here ends conf.
    orden = Order.objects.get(id=pk)
    productos = ArticulosOrdenados.objects.filter(orden=pk)
    #salidas = Salidas.objects.filter(producto__articulos__orden__id=pk)


    #Azul Vordcab
    prussian_blue = Color(0.0859375,0.1953125,0.30859375)
    #prussian_blue = Color(0.2421875,0.5703125,0.796875)
    rojo = Color(0.59375, 0.05859375, 0.05859375)
    c.setFillColor(prussian_blue)
    # REC (DIST DEL MARGEN VERTICAL, DIST DEL MARGEN HORIZONTAL, LARGO DEL RECT, ANCHO DEL RECT)
    c.rect(20,695,565,25, fill=True, stroke=False)


    #Encabezado
    c.setFillColor(black)
    c.setLineWidth(.3)
    c.setFont('Helvetica-Bold',12)
    c.drawString(30,730,'Solicitud:')
    c.setFillColor(rojo)
    c.drawString(90,730,orden.get_folio)
    c.setFillColor(black)
    c.setFont('Helvetica',22)
    c.drawString(30,750,'Vordtec de México')

    c.setFont('Helvetica-Bold',12)
    c.drawString(480,740,orden.created_at.strftime("%d/%m/%Y"))



    c.drawInlineImage('static/images/Logo-Vordtec.png',50,590, 6.0 * cm, 3.0 * cm)
    c.setFillColor(white)
    c.setFont('Helvetica',14)
    c.drawCentredString(320,700,'Comprobante de Solicitud')
    c.setFillColor(black)
    c.setFont('Helvetica',12)
    c.drawString(290,680,'Estatus:')
    c.drawString(290,660, 'Proyecto:')
    c.drawString(290,640, 'Activo:')
    c.drawString(290,620, 'Operación:')
    c.drawString(290,600, 'Sector:')
    c.drawString(290,580, 'Almacén:')

    c.drawString(370,660, orden.proyecto.nombre)
    c.drawString(370,640, orden.activo.eco_unidad)
    c.drawString(370,620, orden.operacion.nombre)
    c.drawString(370,600, orden.sector.nombre)
    c.drawString(370,580, orden.staff.distrito.nombre)


    c.setLineWidth(.3)
    c.line(20,570,585,570)





    #Create blank list
    data =[]

    data.append(['''Código''', '''Nombre''', '''Cantidad'''])


    high = 540
    for producto in productos:
        data.append([producto.producto.producto.codigo, producto.producto.producto.nombre,producto.cantidad])
        high = high - 18


    c.setFillColor(prussian_blue)
    c.rect(20,high-50,565,25, fill=True, stroke=False)
    c.setFillColor(white)
    c.drawCentredString(320,high-45,'Observaciones')
    c.setFillColor(black)
    c.drawCentredString(230,high-190, orden.staff.staff.first_name +' '+ orden.staff.staff.last_name)
    c.line(180,high-195,280,high-195)
    c.drawCentredString(230,high-205, 'Solicitado')
    if orden.sol_autorizada_por == None:
        c.setFillColor(rojo)
        c.drawCentredString(410, high-190, '{Esta orden no ha sido autorizada}')
        c.drawString(370,680, 'No aprobada')
    else:
        c.setFillColor(black)
        c.drawCentredString(410,high-190, orden.sol_autorizada_por.staff.first_name+' '+ orden.staff.staff.last_name)
        c.drawString(370,680, 'Aprobada')
    c.setFillColor(black)
    c.line(360,high-195,460,high-195)
    c.drawCentredString(410,high-205,'Aprobado por')



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
    table = Table(data, colWidths=[4 * cm, 9.0 * cm, 4.0 * cm])
    table.setStyle(TableStyle([ #estilos de la tabla
        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
        ('BOX',(0,0),(-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        #ENCABEZADO
        ('TEXTCOLOR',(0,0),(-1,0), white),
        ('FONTSIZE',(0,0),(-1,0), 13),
        ('BACKGROUND',(0,0),(-1,0), prussian_blue),
        #CUERPO
        ('TEXTCOLOR',(0,1),(-1,-1), colors.black),
        ('FONTSIZE',(0,1),(-1,-1), 12),
        ]))

    #pdf size
    table.wrapOn(c, width, height)
    table.drawOn(c, 55, high)

    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='reporte_' + str(orden.get_folio) +'.pdf')

def reporte_entradas(request):
    entradas = EntradaArticulo.objects.filter(entrada__completo = True, articulo_comprado__producto__producto__articulos__producto__producto__servicio = False)
    myfilter = EntradasFilter(request.GET, queryset=entradas)
    entradas = myfilter.qs

    if request.method == "POST" and 'btnExcel' in request.POST:

        return convert_entradas_to_xls(entradas)


    context = {
        'entradas':entradas,
        'myfilter':myfilter,
        }

    return render(request,'requisiciones/reporte_entradas.html', context)

def reporte_salidas(request):
    salidas = Salidas.objects.filter(salida_firmada = True)
    myfilter = SalidasFilter(request.GET, queryset=salidas)
    salidas = myfilter.qs

    if request.method == "POST" and 'btnExcel' in request.POST:

        return convert_salidas_to_xls(salidas)


    context = {
        'salidas':salidas,
        'myfilter':myfilter,
        }

    return render(request,'requisiciones/reporte_salidas.html', context)

@login_required(login_url='user-login')
def historico_articulos_para_surtir(request):
    registros = ArticulosparaSurtir.history.all()

    context = {
        'registros':registros,
        }

    return render(request,'requisiciones/historicos_articulos_para_surtir.html',context)

@login_required(login_url='user-login')
def historico_salidas(request):
    registros = Salidas.history.all()

    context = {
        'registros':registros,
        }

    return render(request,'requisiciones/historico_salidas.html',context)


def convert_solicitud_autorizada_to_xls(productos):
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

    columns = ['Folio','Solicitante','Proyecto','Subproyecto','Código','Artículo','Creado']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        ws.column_dimensions[get_column_letter(col_num + 1)].width = 16

    columna_max = len(columns)+2

    (ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por Savia V2. UH}')).style = messages_style
    (ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Vordcab S.A. de C.V.}')).style = messages_style

    rows = productos.values_list('articulos__orden_id',Concat('articulos__orden__staff__staff__first_name',Value(' '),'articulos__orden__staff__staff__last_name'),
                            'articulos__orden__proyecto__nombre','articulos__orden__subproyecto__nombre',
                            'articulos__producto__producto__codigo','articulos__producto__producto__nombre','articulos__orden__approved_at')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num/6 >0 and col_num % 6 == 0:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = date_style
            else:
                (ws.cell(row = row_num, column = col_num+1, value=str(row[col_num]))).style = body_style
    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)
    #Aquí termina la implementación del XLSX

def convert_solicitud_autorizada_orden_to_xls(ordenes):
    response= HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename = Solicitudes_pend_requisicion' + str(dt.date.today())+'.xlsx'
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

    columns = ['Folio','Solicitante','Proyecto','Subproyecto','Creado']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        ws.column_dimensions[get_column_letter(col_num + 1)].width = 16

    columna_max = len(columns)+2

    (ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por Savia V2. UH}')).style = messages_style
    (ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Vordcab S.A. de C.V.}')).style = messages_style

    rows = ordenes.values_list('id',Concat('staff__staff__first_name',Value(' '),'staff__staff__last_name'),
                            'proyecto__nombre','subproyecto__nombre','created_at')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            (ws.cell(row = row_num, column = col_num+1, value=str(row[col_num]))).style = body_style
            if col_num == 4:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = date_style

    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)
#Aquí termina la implementación del XLSX

def convert_entradas_to_xls(entradas):
    response= HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename = Entradas_' + str(dt.date.today())+'.xlsx'
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

    columns = ['Folio Solicitud','Fecha','Solicitante','Proyecto','Subproyecto','Código','Articulo','Cantidad']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        ws.column_dimensions[get_column_letter(col_num + 1)].width = 16

    columna_max = len(columns)+2

    (ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por Savia V2. UH}')).style = messages_style
    (ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Vordcab S.A. de C.V.}')).style = messages_style

    rows = entradas.values_list('entrada__oc__req__orden__id','created_at',Concat('entrada__oc__req__orden__staff__staff__first_name',Value(' '),'entrada__oc__req__orden__staff__staff__last_name'),
                        'entrada__oc__req__orden__proyecto__nombre','entrada__oc__req__orden__subproyecto__nombre','articulo_comprado__producto__producto__articulos__producto__producto__codigo',
                        'articulo_comprado__producto__producto__articulos__producto__producto__nombre','cantidad')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            (ws.cell(row = row_num, column = col_num+1, value=str(row[col_num]))).style = body_style
            if col_num == 4:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = date_style

    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)
#Aquí termina la implementación del XLSX

def convert_salidas_to_xls(salidas):
    response= HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename = Salidas_' + str(dt.date.today())+'.xlsx'
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

    columns = ['Folio Solicitud','Fecha','Solicitante','Proyecto','Subproyecto','Código','Articulo','Material recibido por','Cantidad']

    for col_num in range(len(columns)):
        (ws.cell(row = row_num, column = col_num+1, value=columns[col_num])).style = head_style
        ws.column_dimensions[get_column_letter(col_num + 1)].width = 16

    columna_max = len(columns)+2

    (ws.cell(column = columna_max, row = 1, value='{Reporte Creado Automáticamente por Savia V2. UH}')).style = messages_style
    (ws.cell(column = columna_max, row = 2, value='{Software desarrollado por Vordcab S.A. de C.V.}')).style = messages_style

    rows = salidas.values_list('producto__articulos__orden__id','created_at',Concat('producto__articulos__orden__staff__staff__first_name',Value(' '),'producto__articulos__orden__staff__staff__last_name'),
                        'producto__articulos__orden__proyecto__nombre','producto__articulos__orden__subproyecto__nombre','producto__articulos__producto__producto__codigo','producto__articulos__producto__producto__nombre',
                        Concat('material_recibido_por__staff__first_name',Value(' '),'material_recibido_por__staff__last_name'),'cantidad')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            (ws.cell(row = row_num, column = col_num+1, value=str(row[col_num]))).style = body_style
            if col_num == 8:
                (ws.cell(row = row_num, column = col_num+1, value=row[col_num])).style = body_style

    sheet = wb['Sheet']
    wb.remove(sheet)
    wb.save(response)

    return(response)
#Aquí termina la implementación del XLSX