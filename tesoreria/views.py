from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from compras.models import ArticuloComprado, Compra
from compras.forms import CompraForm
from compras.filters import CompraFilter
from compras.views import dof, attach_oc_pdf
from dashboard.models import Subproyecto
from .models import Pago, Cuenta, Facturas
from .forms import PagoForm
from .filters import PagoFilter
from user.models import Profile
from django.contrib import messages
from django.db.models import Sum
from datetime import date, datetime
import decimal
from django.core.mail import EmailMessage



# Create your views here.
@login_required(login_url='user-login')
def compras_autorizadas(request):
    usuario = Profile.objects.get(staff__id=request.user.id)
    if usuario.tipo.tesoreria == True:
        compras = Compra.objects.filter(autorizado2=True, pagada=False).order_by('-folio')
    else:
        compras = Compra.objects.filter(flete=True,costo_fletes='1')
    #compras = Compra.objects.filter(autorizado2=True, pagada=False).order_by('-folio')
    myfilter = CompraFilter(request.GET, queryset=compras)
    compras = myfilter.qs


    context= {
        'compras':compras,
        'myfilter':myfilter,
        }

    return render(request, 'tesoreria/compras_autorizadas.html',context)

@login_required(login_url='user-login')
def compras_pagos(request, pk):
    usuario = Profile.objects.get(staff__id=request.user.id)
    compra = Compra.objects.get(id=pk)
    productos = ArticuloComprado.objects.filter(oc=pk)
    pagos = Pago.objects.filter(oc=compra.id, hecho=True).aggregate(Sum('monto'))
    sub = Subproyecto.objects.get(id=compra.req.orden.subproyecto.id)
    pagos_alt = Pago.objects.filter(oc=compra.id, hecho=True)
    #Esta es otra forma de sacar lo que hice con los pagos, me parece mas legible
    #compra_pagos = compra.pago_set.aggregate(Sum('monto'))

    if pagos['monto__sum'] == None:
            monto_anterior = 0
    else:
        if compra.moneda.nombre == 'PESOS':
            monto_anterior = pagos['monto__sum']
        #cero = Money(0, 'MXN')
        if compra.moneda.nombre == 'DOLARES':
            monto_anterior = pagos['monto__sum']



    if compra.moneda.nombre == 'PESOS':
        cuentas = Cuenta.objects.filter(moneda__nombre = 'PESOS')
    if compra.moneda.nombre == 'DOLARES':
        cuentas = Cuenta.objects.all()


    pago, created = Pago.objects.get_or_create(tesorero = usuario, distrito = usuario.distrito, oc=compra, hecho=False, monto=0)
    form = PagoForm()
    remanente = compra.costo_oc - monto_anterior



    if request.method == 'POST':
        form = PagoForm(request.POST or None, request.FILES or None, instance = pago)
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
        if compra.moneda.nombre == "PESOS":
            sub.gastado = sub.gastado + monto_actual
            cuenta.saldo = cuenta_pagos['monto__sum'] + monto_actual
        if compra.moneda.nombre == "DOLARES":
            if request.POST['monto_1'] == "PESOS": #Si la cuenta es en pesos
                sub.gastado = sub.gastado.amount + monto_actual * decimal.Decimal(request.POST['tipo_de_cambio_0'])
                cuenta.saldo = cuenta_pagos['monto__sum'] + monto_actual * decimal.Decimal(request.POST['tipo_de_cambio_0'])
            if request.POST['monto_1'] == "DOLARES":
                tipo_de_cambio = decimal.Decimal(dof())
                sub.gastado = sub.gastado + monto_actual * tipo_de_cambio
                cuenta.saldo = cuenta_pagos['monto__sum'] + monto_actual
        #actualizar la cuenta de la que se paga
        monto_total= monto_actual + monto_anterior
        compra.monto_pagado = monto_total
        if monto_actual <= 0:
            messages.error(request,f'El pago {monto_actual} debe ser mayor a 0')
        elif monto_total <= compra.costo_oc:
            if form.is_valid():
                if monto_total == compra.costo_oc:
                    compra.pagada= True
                    if compra.cond_de_pago.nombre == "CONTADO":
                        pagos = Pago.objects.filter(oc=compra, hecho=True)
                        archivo_oc = attach_oc_pdf(request, compra.id)
                        if compra.referencia:
                            email = EmailMessage(
                                f'Compra Autorizada {compra.folio}',
                                f'Estimado(a) {compra.proveedor.contacto} | Proveedor {compra.proveedor.nombre}:\n\nEstás recibiendo este correo porque has sido seleccionado para surtirnos la OC adjunta con folio: {compra.folio} y referencia: {compra.referencia}.\n\n Atte. {compra.creada_por.staff.first_name} {compra.creada_por.staff.last_name} \nGrupo Vordcab S.A. de C.V.\n\n Este mensaje ha sido automáticamente generado por SAVIA VORDTEC',
                                'saviax.vordcab@gmail.com',
                                ['ulises_huesc@hotmail.com'],#[compra.proveedor.email],
                                )
                        else:
                            email = EmailMessage(
                                f'Compra Autorizada {compra.folio}',
                                f'Estimado(a) {compra.proveedor.contacto} | Proveedor {compra.proveedor.nombre}:\n\nEstás recibiendo este correo porque has sido seleccionado para surtirnos la OC adjunta con folio: {compra.folio}.\n\n Atte. {compra.creada_por.staff.first_name} {compra.creada_por.staff.last_name} \nGrupo Vordcab S.A. de C.V.\n\n Este mensaje ha sido automáticamente generado por SAVIA VORDTEC',
                                'saviax.vordcab@gmail.com',
                                ['ulises_huesc@hotmail.com'],#[compra.proveedor.email],
                                )
                        email.attach(f'OC_folio_{compra.folio}.pdf',archivo_oc,'application/pdf')
                        email.attach('Pago.pdf',request.FILES['comprobante_pago'].read(),'application/pdf')
                        if pagos.count() > 0:
                            for pago in pagos:
                                email.attach(f'Pago_folio_{pago.id}.pdf',pago.comprobante_pago.path,'application/pdf')
                        email.send()
                        for producto in productos:
                            if producto.producto.producto.articulos.producto.producto.especialista == True:
                                archivo_oc = attach_oc_pdf(request, compra.id)
                                email = EmailMessage(
                                f'Compra Autorizada {compra.folio}',
                                f'Estimado proveedor,\n Estás recibiendo este correo porque ha sido pagada una OC que contiene el producto código:{producto.producto.producto.articulos.producto.producto.codigo} descripción:{producto.producto.producto.articulos.producto.producto.codigo} el cual requiere la liberación de calidad\n Este mensaje ha sido automáticamente generado por SAVIA X',
                                'saviax.vordcab@gmail.com',
                                ['ulises_huesc@hotmail.com'],
                                )
                                email.attach(f'OC_folio:{compra.folio}.pdf',archivo_oc,'application/pdf')
                                email.send()
                pago.save()
                compra.save()
                form.save()
                sub.save()
                cuenta.save()

                messages.success(request,f'Gracias por registrar tu pago, {usuario.staff.first_name}')
                return HttpResponse(status=204) #No content to render nothing and send a "signal" to javascript in order to close window
            else:
                form = PagoForm()
                messages.error(request,f'{usuario.staff.first_name}, No se pudo subir tu documento')
        else:
            messages.error(request,f'{usuario.staff.first_name}, el monto introducido más los pagos anteriores {monto_total} superan el monto total de la OC {compra.costo_oc}')

    context= {
        'compra':compra,
        'pago':pago,
        'form':form,
        'monto':pagos['monto__sum'],
        'suma_pagos': monto_anterior,
        'pagos_alt':pagos_alt,
        'cuentas':cuentas,
        'remanente':remanente,
    }

    return render(request, 'tesoreria/compras_pagos.html',context)

# Create your views here.
@login_required(login_url='user-login')
def matriz_pagos(request):
    pagos = Pago.objects.filter(hecho=True)
    myfilter = PagoFilter(request.GET, queryset=pagos)
    pagos = myfilter.qs

    context= {
        'pagos':pagos,
        'myfilter':myfilter,
        }

    return render(request, 'tesoreria/matriz_pagos.html',context)


@login_required(login_url='user-login')
def matriz_facturas(request, pk):
    compra = Compra.objects.get(id = pk)
    pagos = Pago.objects.filter(oc = compra, hecho=True)
    facturas = None

    context={
        'pagos':pagos,
        'facturas':facturas,
        'compra':compra,
        }

    return render(request, 'tesoreria/matriz_facturas.html', context)

