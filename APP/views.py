from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import *
# Create your views here.
from .forms import HostelForm,MenuForm,RoomForm,FloorForm
from django.db.models import Count
# for the user login and registeration
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group 

# Webpage Home view
@login_required(login_url='login')
def hostel(request):
    hostel = Hostel.objects.all()
    context = {
        "hostel": hostel
    }
    return render(request,'index.html',context)

# Menu web page view
@login_required(login_url='login')
def menu(request):
    menu = Menu.objects.all()
    context = {
        "menu":menu
    }
    return render(request,'menu.html',context)

# Reviews page at the web page
@login_required(login_url='login')
def reviews(request):
    return render(request,'Review.html')

# About us page for the web page
@login_required(login_url='login')
def aboutus(request):
    return render(request,'about_us.html')

# Login view for the login procedure
@unauthenticated_user
def login_view(request):
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

# For the logout process
def logoutUser(request):
    logout(request)
    return redirect('login')

#For the resgisteration page
@unauthenticated_user
def register(request): 
    form = CreateUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')
        group = Group.objects.get(name='student')
        user.groups.add(group)
        Userprofile.objects.create(
            user= user,
            name=username
        )
        return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html',context)

# User page
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def userpage(request):
    booking = Booking.objects.select_related('room__floor__hostel').filter(user=request.user).first()
    context ={
        'booking': booking,
        
    }
    return render(request,'admin_view/userpage.html',context)

#User Setting
def usersetting(request):
    context = {
    }
    return render(request,'admin_view/user_setting.html',context)


#Dashboard for the admin view
@login_required(login_url='login')
@admin_only
def dashboard(request):
    user = Userprofile.objects.all()
    bookings = Booking.objects.select_related('user', 'room', 'room__floor', 'room__floor__hostel')
    room = Room.objects.select_related('floor','floor__hostel')
    total_user = Userprofile.objects.count()
    total_hostel = Hostel.objects.count()
    total_room  = Room.objects.count()
    total_booking = Booking.objects.count()
    total_floor = Floor.objects.count()
    room_M = room.filter(status='Maintainece')
    room_F = room.filter(status='Full')
    context ={
        'bookings': bookings,
        'user_count': total_user,
        'hostel_count': total_hostel,
        'room_count': total_room,
        'booking_count': total_booking,
        'floor_count': total_floor,
        'maintain': room_M,
        'full': room_F,
        'user': user,

    }
    return render (request,'admin_view/dashboard.html',context= context)

# Student profile at the admin page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def student_profile(request,pk_test):
    userprofile = get_object_or_404(Userprofile, id=pk_test)
    bookings = Booking.objects.filter(user=userprofile.user).select_related('room__floor__hostel')
    context ={
        'users': userprofile,
        'booking':bookings,
    }
    return render(request,'admin_view/student_profile.html',context)

# Hostel view at admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def hostel_detail(request,pk):
    hostel = get_object_or_404(Hostel, id=pk)
    floor = hostel.floors.prefetch_related('rooms')

    context ={
        'hostel': hostel,
        'floor': floor,
    }
    return render(request,'admin_view/hostel_detail.html',context)
#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_hostel (request,pk):
    hostel = get_object_or_404(Hostel, id=pk)
    if request.method == 'POST':
        hostel.delete()
        return redirect('hostel')
    context = {
        'hostel': hostel

    }
    return render(request,'admin_view/hostel_delete.html',context)

# Menu admin page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def menu_admin(request):
    menu = Menu.objects.all()
    context ={
        'menu': menu
    }
    return render(request,'admin_view/menu.html',context)
#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def menu_delete(request,pk):
    menu = get_object_or_404(Menu, id=pk)
    if request.method == 'POST':
        menu.delete()
        return redirect('menu_admin')
    context = {
        'menu': menu

    }
    return render(request,'admin_view/menu_delete.html',context)


#For the room CRUD functions
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_room(request, pk):
    floor = get_object_or_404(Floor, id=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.floor = floor
            room.save()
            return redirect('hostel_detail', pk=floor.hostel.id)  # Ensure this is the correct URL pattern name
    else:
        form = RoomForm()
    
    context = {
        'form': form,
        'floor': floor,
    }
    return render(request, 'admin_view/room_form.html', context)
#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_room(request,pk):
    room = get_object_or_404(Room, id=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('hostel')  # Ensure this is the correct URL pattern name
    else:
        form = RoomForm(instance=room)
    
    context = {
        'form': form,
    }
    return render(request, 'admin_view/room_form.html', context)
#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_room(request,pk):
    room = get_object_or_404(Room, id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('hostel')
    context = {
        'room': room
    }
    return render(request,'admin_view/room_delete.html',context)

# For the floor CRUD functions

#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_floor(request,pk):
    hostel = get_object_or_404(Hostel,id = pk)
    if request.method == 'POST':
        form = FloorForm(request.POST)
        if form.is_valid():
            floor = form.save(commit=False)
            floor.hostel = hostel
            floor.save()
            return redirect('hostel_detail', pk = hostel.id)  # Ensure this is the correct URL pattern name
    else:
        form = FloorForm()
    
    context={
        'form': form,
        'hostel': hostel,
    }
    return render(request,'admin_view/floor_form.html',context)

#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_floor(request,pk):
    floor = get_object_or_404(Floor, id=pk)
    if request.method == 'POST':
        form = FloorForm(request.POST, request.FILES, instance=floor)
        if form.is_valid():
            form.save()
            return redirect('hostel')  # Ensure this is the correct URL pattern name
    else:
        form = FloorForm(instance=floor)
    
    context = {
        'floor': floor,
        'form': form,
    }
    return render(request, 'admin_view/floor_form.html', context)

#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_floor(request,pk):
    floor = get_object_or_404(Floor, id=pk)
    if request.method == 'POST':
        floor.delete()
        return redirect('hostel')
    context = {
        'floor': floor
    }
    return render(request,'admin_view/floor_delete.html',context)

# For the booking view at the admin page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def booking_admin(request):
    hostel = Hostel.objects.all()
    context = {
        'hostel': hostel,
    }
    return render(request, 'admin_view/booking.html',context)

#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def booking_detail(request,pk):
    hostel = get_object_or_404(Hostel, id=pk)
    bookings = Booking.objects.filter(room__floor__hostel=hostel)
    
    context = {
        'hostel': hostel,
        'booking': bookings,
    }
    return render(request, 'admin_view/booking_detail.html', context)
#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_booking(request,pk):
    booking = get_object_or_404(Booking, id=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_admin')
    context = {
        'booking': booking
    }
    return render(request,'admin_view/booking_delete.html',context)




    

    

    
    


