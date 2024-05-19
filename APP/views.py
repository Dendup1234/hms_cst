from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Hostel,Menu
# Create your views here.

@login_required(login_url='login')
def hostel(request):
    hostel = Hostel.objects.all()
    context = {
        "hostel": hostel
    }
    return render(request,'index.html',context)

@login_required(login_url='login')
def menu(request):
    menu = Menu.objects.all()
    context = {
        "menu":menu
    }
    return render(request,'menu.html',context)

@login_required(login_url='login')
def reviews(request):
    return render(request,'Review.html')

@login_required(login_url='login')
def aboutus(request):
    return render(request,'about_us.html')

# for the user login and registeration
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
     if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(request, username=username, password=password)
         if user is not None:
             auth_login(request, user)
             return redirect('home')
         else:
             messages.info(request,'Username Or password is incorrect')
            

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
     form = CreateUserForm(request.POST)
     if form.is_valid():
         form.save()
         user = form.cleaned_data.get('username')
         messages.success(request,'Account was created for '+ user)
         return redirect('login')
     context={'form':form}
     return render(request,'accounts/register.html',context)

