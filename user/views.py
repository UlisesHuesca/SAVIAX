from django.shortcuts import render, redirect
#Estamos importando la "Form" de default de Django para crear usuarios
#from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm

# Create your views here.
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
    return render(request, 'user/profile.html')
