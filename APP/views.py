from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import *
# Create your views here.
from .forms import HostelForm,MenuForm
from django.db.models import Count
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

#
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
#
def logoutUser(request):
    logout(request)
    return redirect('login')
#
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

#
def dashboard(request):
    user = User.objects.all()
    bookings = Booking.objects.select_related('user', 'room', 'room__floor', 'room__floor__hostel')
    room = Room.objects.select_related('floor','floor__hostel')
    total_user = User.objects.count()
    total_hostel = Hostel.objects.count()
    total_room  = Room.objects.count()
    total_booking = Booking.objects.count()
    room_M = room.filter(status='Maintainece')
    room_F = room.filter(status='Full')
    context ={
        'bookings': bookings,
        'user_count': total_user,
        'hostel_count': total_hostel,
        'room_count': total_room,
        'booking_count': total_booking,
        'maintain': room_M,
        'full': room_F,
        'user': user,

    }
    return render (request,'admin_view/dashboard.html',context= context)

#
def student_profile(request,pk_test):
    user = User.objects.get(reg_number= pk_test)
    bookings = Booking.objects.filter(user=user).select_related('room__floor__hostel')

    context ={
        'user': user,
        'booking':bookings
    }
    return render(request,'admin_view/student_profile.html',context)

#
def hostel_admin_view(request):
    hostels = Hostel.objects.all().annotate(
        floor_count=Count('floors', distinct=True),
        room_count=Count('floors__rooms', distinct=True)
    )
    context ={
        'hostel': hostels
    }
    return render(request,'admin_view/hostel.html',context)

#
def create_hostel(request):
    if request.method == 'POST':
        form = HostelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hostel')  # Ensure this is the correct URL pattern name
    else:
        form = HostelForm()
    
    context = {
        'form': form,
    }
    return render(request, 'admin_view/hostel_form.html', context)
#
def update_hostel(request, pk):
    hostel = get_object_or_404(Hostel, id=pk)
    if request.method == 'POST':
        form = HostelForm(request.POST, request.FILES, instance=hostel)
        if form.is_valid():
            form.save()
            return redirect('hostel')  # Ensure this is the correct URL pattern name
    else:
        form = HostelForm(instance=hostel)
    
    context = {
        'form': form,
    }
    return render(request, 'admin_view/hostel_form.html', context)
#
def delete_hostel (request,pk):
    hostel = get_object_or_404(Hostel, id=pk)
    if request.method == 'POST':
        hostel.delete()
        return redirect('hostel')
    context = {
        'hostel': hostel

    }
    return render(request,'admin_view/hostel_delete.html',context)
#
def menu_admin(request):
    menu = Menu.objects.all()
    context ={
        'menu': menu
    }
    return render(request,'admin_view/menu.html',context)
#
def menu_create(request):
    form = MenuForm
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_admin')  # Ensure this is the correct URL pattern name
    else:
        form = MenuForm()
    context={
        'form': form
    }
    return render(request,'admin_view/menu_form.html',context)
# 
def menu_update(request,pk):
    menu = get_object_or_404(Menu, id=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('menu_admin')  # Ensure this is the correct URL pattern name
    else:
        form = MenuForm(instance=menu)
    
    context = {
        'form': form,
    }
    return render(request, 'admin_view/menu_form.html', context)
    
    


