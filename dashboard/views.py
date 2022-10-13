from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import ArticulosparaSurtir
from .models import Product, Subfamilia, Order, Products_Batch, Familia, Unidad
from solicitudes.models import Subproyecto
from requisiciones.models import Salidas, ValeSalidas
from user.models import Profile
from .forms import ProductForm, Products_BatchForm, AddProduct_Form
from django.contrib.auth.models import User
from .filters import ProductFilter
from django.contrib import messages
import csv
from django.core.paginator import Paginator
from django.db.models import Sum
#import decimal

# Create your views here.
@login_required(login_url='user-login')
def index(request):
    usuario = Profile.objects.get(id=request.user.id)
    #vale_salidas = ValeSalidas.objects.filter(material_recibido_por = usuario)
    #salidas = Salidas.objects.filter(vale_salida = vale_salidas) | No jala me marca que la búsqueda por un valor exacto debe estar limtado a un resultado no debería ser porque hay 3
    subproyectos = Subproyecto.objects.all()
    #productos = Inventario.objects.filter(producto = salidas.producto.articulos.producto.producto)
    labels = []
    data = []
    subproy = []
    gast = []
    pres = []


    #for salida in salidas:
    #    if salida.producto.articulos.producto.producto.nombre not in labels:
    #        labels.append(salida.producto.articulos.producto.producto.nombre)
    #        data.append(salida.cantidad)
    #    else:
    #        index = labels.index(salida.producto.articulos.producto.producto.nombre)
    #        data[index] = data[index]+salida.cantidad

    for subproyecto in subproyectos:
        subproy.append(subproyecto.nombre)
        gast.append(format(subproyecto.gastado.amount, '.2f'))
        pres.append(format(subproyecto.presupuesto.amount, '.2f'))

    context= {
        'usuario':usuario,
        'labels':labels,
        'data':data,
        'subproyecto':subproy,
        'gastado':gast,
        }
    return render(request,'dashboard/index.html',context)

@login_required(login_url='user-login')
def staff(request):
    workers = User.objects.all()
    context= {
        'workers': workers,
        }
    return render(request,'dashboard/staff.html', context)

@login_required(login_url='user-login')
def product(request):
    items = Product.objects.filter(completado = True).order_by('codigo')

    myfilter=ProductFilter(request.GET, queryset=items)
    items = myfilter.qs

    #Set up pagination
    p = Paginator(items, 50)
    page = request.GET.get('page')
    items_list = p.get_page(page)

    context = {
        'items': items,
        'myfilter':myfilter,
        'items_list':items_list,
        }


    return render(request,'dashboard/product.html', context)


@login_required(login_url='user-login')
def upload_batch_products(request):

    form = Products_BatchForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        form = Products_BatchForm()
        product_list = Products_Batch.objects.get(activated = False)
        f = open(product_list.file_name.path, 'r')
        reader = csv.reader(f)
        next(reader) #Advance past the reader

        for row in reader:
            if not Product.objects.filter(codigo=row[0]):
                if Unidad.objects.get(nombre = row[2]):
                    unidad = Unidad.objects.get(nombre = row[2])
                    if Familia.objects.get(nombre = row[3]):
                        familia = Familia.objects.get(nombre = row[3])
                        if Subfamilia.objects.get(nombre = row[4], familia = familia):
                            subfamilia = Subfamilia.objects.get(nombre = row[4], familia = familia)
                            producto = Product(codigo=row[0],nombre=row[1], unidad=unidad, familia=familia, subfamilia=subfamilia,especialista=row[5],iva=row[6],activo=row[7],servicio=row[8],baja_item=False,completado=True)
                            producto.save()
                        else:
                            messages.error(request,f'La subfamilia no existe dentro de la base de datos, producto:{row[0]}')
                    else:
                        messages.error(request,f'La familia no existe dentro de la base de datos, producto:{row[0]}')
                else:
                    messages.error(request,f'La unidad no existe dentro de la base de datos, producto:{row[0]}')
            else:
                messages.error(request,f'El producto código:{row[0]} ya existe dentro de la base de datos')

        product_list.activated = True
        product_list.save()


    context = {
        'form': form,
        }

    return render(request,'dashboard/upload_batch_products.html', context)


@login_required(login_url='user-login')
def order(request):
    orders = Order.objects.all()
    context= {
        'orders':orders,
        }

    return render(request,'dashboard/order.html', context)

@login_required(login_url='user-login')
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')

    return render(request,'dashboard/product_delete.html')


@login_required(login_url='user-login')
def add_product(request):
    item, created = Product.objects.get_or_create(completado=False)

    if request.method =='POST':
        form = AddProduct_Form(request.POST, request.FILES or None, instance = item)
        form.save(commit=False)
        item.completado = True
        if form.is_valid():
            form.save()
            item.save()
            messages.success(request,f'Has agregado correctamente el producto {item.nombre}')
            return redirect('dashboard-product')
    else:
        form = AddProduct_Form()


    context = {
        'form': form,
        'item':item,
        }
    return render(request,'dashboard/add_product.html', context)

@login_required(login_url='user-login')
def product_update(request, pk):
#def product_update_modal(request, pk):

    item = Product.objects.get(id=pk)

    if request.method =='POST':
        form = AddProduct_Form(request.POST, request.FILES or None, instance=item, )
        if form.is_valid():
            form.save()
            messages.success(request,f'Has actualizado correctamente el producto {item.nombre}')
            return redirect('dashboard-product')
    else:
        form = AddProduct_Form(instance=item)


    context = {
        'form': form,
        'item':item,
        }
    return render(request,'dashboard/product_update.html', context)



def load_subfamilias(request):

    familia_id = request.GET.get('familia_id')
    subfamilias = Subfamilia.objects.filter(familia_id = familia_id)

    return render(request, 'dashboard/subfamilia_dropdown_list_options.html',{'subfamilias': subfamilias})


@login_required(login_url='user-login')
def staff_detail(request, pk):
    worker = User.objects.get(id=pk)
    context={
        'worker': worker,
        }
    return render(request,'dashboard/staff_detail.html', context)
