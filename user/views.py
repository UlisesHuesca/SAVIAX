from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from .models import Profile
from .forms import Profile_Form
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='user-login')
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form = UserForm()
    ctx = {
        'form':form,
        }
    return render(request, 'user/register.html',ctx)

def profile(request):
    perfil = Profile.objects.get(staff__id=request.user.id)

    context ={
        'perfil':perfil,
    }

    return render(request, 'user/profile.html', context)

@login_required(login_url='user-login')
def edit_profile(request):
    perfil = Profile.objects.get(staff__id=request.user.id)
    #perfil = Profile.objects.get(id = pk)
    #custom_user = CustomUser.objects.get(staff = perfil.staff.staff)
    form = Profile_Form(instance=perfil)
    error_messages = {}

    if request.method == "POST":
        form = Profile_Form(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            custom_user = form.save()
            messages.success(request,f'Tu perfil se ha actualizado correctamente, {perfil.staff.first_name}')
            return redirect('user-profile')
        else:
            for field, errors in form.errors.items():
                error_messages[field] = errors.as_text()


    context = {
        'error_messages': error_messages,
        'form':form,
        'perfil':perfil,
    }

    return render(request, 'user/edit_profile.html', context)