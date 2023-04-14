from django.shortcuts import render, redirect
from datetime import date, datetime
from django.contrib import messages
from django.core.mail import EmailMessage
from dashboard.models import Inventario
from solicitudes.models import Proyecto, Subproyecto, Operacion
from tesoreria.models import Pago, Cuenta
from .models import Solicitud_Gasto, Articulo_Gasto
from .forms import Solicitud_GastoForm, Articulo_GastoForm, Articulo_Gasto_Edit_Form, Pago_Gasto_Form
from compras.views import attach_oc_pdf
from .filters import Solicitud_Gasto_Filter
from user.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Sum
import json
import decimal

# Create your views here.
@login_required(login_url='user-login')
def crear_gasto(request):
    usuario = Profile.objects.get(staff__id=request.user.id)
    superintendentes = Profile.objects.filter(tipo__superintendente=True)
    #Tengo que revisar primero si ya existe una orden pendiente del usuario
    gasto, created = Solicitud_Gasto.objects.get_or_create(complete= False)

    productos = Articulo_Gasto.objects.filter(gasto=gasto)

    articulos_gasto = Inventario.objects.filter(producto__gasto = True)
    articulos = Inventario.objects.filter(producto__gasto = False)
    form_product = Articulo_GastoForm()




    if request.method =='POST' and "agregar" in request.POST:
        form = Solicitud_GastoForm(request.POST, instance=gasto)
        gasto = form.save(commit=False)
        gasto.complete = True
        gasto.created_at = date.today()
        gasto.created_at_time = datetime.now().time()
        gasto.staff =  usuario
        #abrev= usuario.distrito.abreviado
        if form.is_valid():
            gasto.save()
            messages.success(request, f'La solicitud {gasto.id} ha sido creada')
            return redirect('solicitudes-gasto')
    else:
        form = Solicitud_GastoForm()


    context= {
        'productos':productos,
        'form':form,
        'form_product': form_product,
        'articulos':articulos,
        'articulos_gasto':articulos_gasto,
        'gasto':gasto,
        'superintendentes':superintendentes,
    }
    return render(request, 'gasto/crear_gasto.html', context)

def update_gasto(request):
    #gasto_id,producto_id,descripion,val_cantidad,val_precio,action
    data= json.loads(request.body)
    action = data["action"]
    producto_id = data["producto_id"]

    if action == "add":
        gasto_id = data["gasto_id"]
        descripcion = data["descripcion"]
        precio = data["val_precio"]
        check = data['check']
        producto = Inventario.objects.get(id=producto_id)
        gasto = Solicitud_Gasto.objects.get(id = gasto_id)
        cantidad = data["val_cantidad"]
        check_express = data['check_express']
        articulo, created = Articulo_Gasto.objects.get_or_create(clase=check, producto = producto, comentario = descripcion, gasto = gasto, cantidad = cantidad, precio_unitario = precio, entrada_salida_express = check_express)
        messages.success(request,f'Has agregado el artículo {articulo} correctamente')
        articulo.save()
    if action == "remove":
        articulo = Articulo_Gasto.objects.get(id=producto_id)
        messages.success(request,f'Has eliminado el artículo {articulo} correctamente')
        articulo.delete()

    return JsonResponse('Item updated, action executed: '+data["action"], safe=False)

def editar_gasto(request, pk):
    producto = Articulo_Gasto.objects.get(id=pk)

    form = Articulo_Gasto_Edit_Form(instance=producto)

    if request.method =='POST':
        form = Articulo_Gasto_Edit_Form(request.POST, instance=producto)

        if form.is_valid():
            form.save()

            messages.success(request,f'Se ha guardado el artículo {producto} correctamente')
            return HttpResponse(status=204)
        #else:
            #messages.error(request,'Se lo llevo SPM')


    context= {
        'producto': producto,
        'form': form,
        }

    return render(request, 'gasto/editar_gasto.html', context)

@login_required(login_url='user-login')
def solicitudes_gasto(request):

    #obtengo el id de usuario, lo paso como argumento a id de profiles para obtener el objeto profile que coindice con ese usuario_id
    perfil = Profile.objects.get(staff__id=request.user.id)


    #Este es un filtro por perfil supervisor o superintendente, es decir puede ver todo lo del distrito
    #if perfil.tipo.superintendente == True:
    #    solicitudes = Solicitud_Gasto.objects.filter(complete=True, staff__distrito=perfil.distrito).order_by('-folio')
    #elif perfil.tipo.supervisor == True:
    #    solicitudes = Solicitud_Gasto.objects.filter(complete=True, staff__distrito=perfil.distrito, supervisor=perfil).order_by('-folio')
    #else:
    solicitudes = Solicitud_Gasto.objects.filter(complete=True, staff = perfil).order_by('-folio')

    myfilter=Solicitud_Gasto_Filter(request.GET, queryset=solicitudes)
    solicitudes = myfilter.qs

    #Set up pagination
    p = Paginator(solicitudes, 10)
    page = request.GET.get('page')
    ordenes_list = p.get_page(page)

    #if request.method =='POST' and 'btnExcel' in request.POST:

        #return convert_excel_solicitud_matriz(solicitudes)

    context= {
        'ordenes_list':ordenes_list,
        'myfilter':myfilter,
        }

    return render(request, 'gasto/solicitudes_gasto.html',context)

@login_required(login_url='user-login')
def detalle_gastos(request, pk):
    productos = Articulo_Gasto.objects.filter(gasto__id=pk)

    context= {
        'productos':productos,
        }

    return render(request, 'gasto/detalle_gasto.html', context)

@login_required(login_url='user-login')
def gastos_pendientes_autorizar(request):

    #obtengo el id de usuario, lo paso como argumento a id de profiles para obtener el objeto profile que coindice con ese usuario_id
    perfil = Profile.objects.get(staff__id=request.user.id)

    #Este es un filtro por perfil supervisor o superintendente, es decir puede ver todo lo del distrito
    #if perfil.tipo.superintendente == True:
    #    solicitudes = Solicitud_Gasto.objects.filter(complete=True, staff__distrito=perfil.distrito).order_by('-folio')
    #elif perfil.tipo.supervisor == True:
    #    solicitudes = Solicitud_Gasto.objects.filter(complete=True, staff__distrito=perfil.distrito, supervisor=perfil).order_by('-folio')
    #else:
    solicitudes = Solicitud_Gasto.objects.filter(complete=True, autorizar = None).order_by('-folio')

    myfilter=Solicitud_Gasto_Filter(request.GET, queryset=solicitudes)
    solicitudes = myfilter.qs

    #Set up pagination
    p = Paginator(solicitudes, 10)
    page = request.GET.get('page')
    ordenes_list = p.get_page(page)

    #if request.method =='POST' and 'btnExcel' in request.POST:

        #return convert_excel_solicitud_matriz(solicitudes)

    context= {
        'ordenes_list':ordenes_list,
        'myfilter':myfilter,
        }

    return render(request, 'gasto/pendientes_autorizar_gasto.html', context)

@login_required(login_url='user-login')
def autorizar_gasto(request, pk):
    perfil = Profile.objects.get(staff__id=request.user.id)
    gasto = Solicitud_Gasto.objects.get(id = pk)
    productos = Articulo_Gasto.objects.filter(gasto = gasto)

    if request.method =='POST':
        gasto.autorizar = True
        gasto.approved_at = date.today()
        gasto.approved_at_time = datetime.now().time()
        gasto.sol_autorizada_por = Profile.objects.get(staff__id=request.user.id)
        gasto.save()
        messages.success(request, f'{perfil.staff.first_name} has autorizado la solicitud {gasto.id}')
        return redirect ('gastos-pendientes-autorizar')


    context = {
        'gasto': gasto,
        'productos': productos,
    }

    return render(request,'gasto/autorizar_gasto.html', context)


@login_required(login_url='user-login')
def cancelar_gasto(request, pk):
    perfil = Profile.objects.get(staff__id=request.user.id)
    gasto = Solicitud_Gasto.objects.get(id = pk)
    productos = Articulo_Gasto.objects.filter(gasto = gasto)

    if request.method =='POST':
        gasto.autorizar = False
        gasto.approved_at = date.today()
        gasto.approved_at_time = datetime.now().time()
        gasto.sol_autorizada_por = Profile.objects.get(staff__id=request.user.id)
        gasto.save()
        messages.info(request, f'{perfil.staff.first_name} has cancelado la solicitud {gasto.id}')
        return redirect ('gastos-pendientes-autorizar')


    context = {
        'gasto': gasto,
        'productos': productos,
    }

    return render(request,'gasto/cancelar_gasto.html', context)

# Create your views here.
@login_required(login_url='user-login')
def pago_gastos_autorizados(request):
    usuario = Profile.objects.get(staff__id=request.user.id)

    if usuario.tipo.tesoreria == True:
        gastos = Solicitud_Gasto.objects.filter(autorizar=True, pagada=False).order_by('-folio')


    myfilter = Solicitud_Gasto_Filter(request.GET, queryset=gastos)
    gastos = myfilter.qs


    context= {
        'gastos':gastos,
        'myfilter':myfilter,
        }

    return render(request, 'gasto/pago_gastos_autorizados.html',context)

@login_required(login_url='user-login')
def pago_gasto(request, pk):
    usuario = Profile.objects.get(staff__id=request.user.id)
    gasto = Solicitud_Gasto.objects.get(id=pk)
    pagos = Pago.objects.filter(gasto=gasto, hecho=True).aggregate(Sum('monto'))
    sub = Subproyecto.objects.get(id=gasto.subproyecto.id)
    pagos_alt = Pago.objects.filter(gasto=gasto, hecho=True)

    if pagos['monto__sum'] == None:
        monto_anterior = 0
    else:
        monto_anterior = pagos['monto__sum']

    cuentas = Cuenta.objects.filter(moneda__nombre = 'PESOS')

    pago, created = Pago.objects.get_or_create(tesorero = usuario, distrito = usuario.distrito, gasto=gasto, hecho=False, monto=0)
    form = Pago_Gasto_Form()
    remanente = gasto.get_total_solicitud - monto_anterior



    if request.method == 'POST':
        form = Pago_Gasto_Form(request.POST or None, request.FILES or None, instance = pago)
        pago = form.save(commit = False)
        pago.pagado_date = date.today()
        pago.pagado_hora = datetime.now().time()
        pago.hecho = True
        #Traigo la cuenta que se capturo en el form
        cuenta = Cuenta.objects.get(cuenta = pago.cuenta.cuenta)
        #La utilizo para sacar la información de todos los pagos relacionados con esa cuenta y sumarlos
        cuenta_pagos = Pago.objects.filter(cuenta = pago.cuenta).aggregate(Sum('monto'))
        if cuenta_pagos['monto__sum'] == None:
            cuenta_pagos['monto__sum']=0

        # Actualizo el saldo de la cuenta
        monto_actual = decimal.Decimal(pago.monto) #request.POST['monto_0']
        sub.gastado = sub.gastado + monto_actual
        cuenta.saldo = cuenta_pagos['monto__sum'] + monto_actual
        monto_total= monto_actual + monto_anterior
        if monto_actual <= 0:
            messages.error(request,f'El pago {monto_actual} debe ser mayor a 0')
        elif monto_total <= gasto.get_total_solicitud:
            if form.is_valid():
                if monto_total == gasto.get_total_solicitud:
                    gasto.pagada = True
                    pagos = Pago.objects.filter(gasto=gasto, hecho=True)
                    #archivo_oc = attach_oc_pdf(request, gasto.id)
                    email = EmailMessage(
                        f'Gasto Autorizado {gasto.id}',
                        f'Estimado(a) {gasto.staff.staff}:\n\nEstás recibiendo este correo porque ha sido pagada el gasto con folio: {gasto.id}.\n\n\nGrupo Vordcab S.A. de C.V.\n\n Este mensaje ha sido automáticamente generado por SAVIA VORDTEC',
                        'saviax.vordcab@gmail.com',
                        ['ulises_huesc@hotmail.com'],#[compra.proveedor.email],
                        )
                    #email.attach(f'OC_folio_{gasto.id}.pdf',archivo_oc,'application/pdf')
                    email.attach('Pago.pdf',request.FILES['comprobante_pago'].read(),'application/pdf')
                    if pagos.count() > 0:
                        for pago in pagos:
                            email.attach(f'Pago_folio_{pago.id}.pdf',pago.comprobante_pago.path,'application/pdf')
                    email.send()
                pago.save()
                gasto.save()
                form.save()
                sub.save()
                cuenta.save()
                messages.success(request,f'Gracias por registrar tu pago, {usuario.staff.first_name}')
                return HttpResponse(status=204) #No content to render nothing and send a "signal" to javascript in order to close window
            else:
                form = Pago_Gasto_Form()
                messages.error(request,f'{usuario.staff.first_name}, No se pudo subir tu documento')
        else:
            messages.error(request,f'{usuario.staff.first_name}, el monto introducido más los pagos anteriores {monto_total} superan el monto total del gasto')

    context= {
        'gasto':gasto,
        'pago':pago,
        'form':form,
        'suma_pagos': monto_anterior,
        'pagos_alt':pagos_alt,
        'cuentas':cuentas,
        'remanente':remanente,
    }

    return render(request,'gasto/pago_gasto.html',context)


