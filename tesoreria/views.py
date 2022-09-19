from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from compras.models import ArticuloComprado, Compra
from compras.forms import CompraForm
from compras.filters import CompraFilter
from compras.views import dof, attach_oc_pdf
from dashboard.models import Subproyecto
from .models import Pago, Cuenta
from .forms import PagoForm
from .filters import PagoFilter
from user.models import Profile
from django.contrib import messages
from django.db.models import Sum
from datetime import date, datetime
from djmoney.money import Money
from decimal import Decimal
from django.core.mail import EmailMessage



# Create your views here.
@login_required(login_url='user-login')
def compras_autorizadas(request):
    compras = Compra.objects.filter(autorizado2=True, pagada=False).order_by('-folio')
    myfilter = CompraFilter(request.GET, queryset=compras)
    compras = myfilter.qs


    context= {
        'compras':compras,
        'myfilter':myfilter,
        }

    return render(request, 'tesoreria/compras_autorizadas.html',context)

@login_required(login_url='user-login')
def compras_pagos(request, pk):
    usuario = Profile.objects.get(id=request.user.id)
    compra = Compra.objects.get(id=pk)
    pagos = Pago.objects.filter(oc=compra.id, hecho=True).aggregate(Sum('monto'))
    sub = Subproyecto.objects.get(id=compra.req.orden.subproyecto.id)
    pagos_alt = Pago.objects.filter(oc=compra.id, hecho=True)
    #Esta es otra forma de sacar lo que hice con los pagos, me parece mas legible
    #compra_pagos = compra.pago_set.aggregate(Sum('monto'))

    if pagos['monto__sum'] == None:
            monto_anterior = 0
    else:
        if compra.moneda.nombre == 'Pesos':
            monto_anterior = Money(pagos['monto__sum'], 'MXN')
        #cero = Money(0, 'MXN')
        if compra.moneda.nombre == 'Dólares':
            monto_anterior = Money(pagos['monto__sum'], 'USD')



    if compra.moneda.nombre == 'Pesos':
        cuentas = Cuenta.objects.filter(moneda__nombre = 'Pesos')
    if compra.moneda.nombre == 'Dólares':
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
        #Agarré el valor directo del post y lo convertí a Money porque marcaba como error la no existencía de pago.monto
        monto_actual = Money(request.POST['monto_0'], request.POST['monto_1'])
        if compra.moneda.nombre == "Pesos":
            sub.gastado = sub.gastado + monto_actual
            cuenta.saldo = Money(cuenta_pagos['monto__sum'], 'MXN') + monto_actual
        if compra.moneda.nombre == "Dólares":
            if request.POST['monto_1'] == "Pesos": #Si la cuenta es en pesos
                sub.gastado = sub.gastado.amount + monto_actual.amount * Decimal(request.POST['tipo_de_cambio_0'])
                cuenta.saldo = Money(cuenta_pagos['monto__sum'], 'MXN') + monto_actual * Decimal(request.POST['tipo_de_cambio_0'])
            if request.POST['monto_1'] == "Dólares":
                tipo_de_cambio = Decimal(dof())
                sub.gastado = sub.gastado.amount + monto_actual.amount * tipo_de_cambio
                cuenta.saldo = Money(cuenta_pagos['monto__sum'], 'USD') + monto_actual
        #actualizar la cuenta de la que se paga
        monto_total= monto_actual + monto_anterior
        compra.monto_pagado = monto_total
        if monto_actual.amount <= 0:
            messages.error(request,f'El pago {monto_actual} debe ser mayor a 0')
        elif monto_total <= compra.costo_oc:
            if form.is_valid():
                if monto_total == compra.costo_oc:
                    compra.pagada= True
                    if compra.cond_de_pago.nombre == "Contado":
                        pagos = Pago.objects.filter(oc=compra, hecho=True)
                        archivo_oc = attach_oc_pdf(request, compra.id)
                        email = EmailMessage(
                            f'Compra Autorizada {compra.folio}',
                            f'Estimado {compra.proveedor.contacto} | Proveedor {compra.proveedor.nombre}:,\n Estás recibiendo este correo porque has sido seleccionado para surtirnos la compra con folio: {compra.folio}.\n\n Este mensaje ha sido automáticamente generado por SAVIA X',
                            'saviax.vordcab@gmail.com',
                            [compra.proveedor.email],
                            )
                        email.attach(f'OC_folio_{compra.folio}.pdf',archivo_oc,'application/pdf')
                        email.attach('Pago.pdf',request.FILES['comprobante_pago'].read(),'application/pdf')
                        if pagos.count() > 0:
                            for pago in pagos:
                                email.attach(f'Pago_folio_{pago.id}.pdf',pago.comprobante_pago.path,'application/pdf')
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
