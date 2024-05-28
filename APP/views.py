from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import *
from .forms import HostelForm,MenuForm,RoomForm,FloorForm,BookingForm,ReviewForm,CounselorForm
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group 
from django.db.models import Avg

# Webpage Home view
@login_required(login_url='login')
def hostel(request):
    male_hostels = Hostel.objects.filter(gender='M').annotate(average_rating=Avg('reviews__reviews'), review_count=Count('reviews'))
    female_hostels = Hostel.objects.filter(gender='F').annotate(average_rating=Avg('reviews__reviews'), review_count=Count('reviews'))
    context = {
        "male_hostels": male_hostels,
        "female_hostels": female_hostels,
    }
    return render(request,'index.html',context)

# Floor view for the selected hostel
@login_required(login_url='login')
def seleted_floor(request, pk):
    hostel = get_object_or_404(Hostel, id=pk)
    floor = hostel.floors.all()
    context={
        'hostel': hostel,
        'floor': floor,
    }
    return render(request,'floor.html',context)
# Selected room for the floor of the given hostel
@login_required(login_url='login')
def selected_room(request,pk):
    floor = get_object_or_404(Floor, id= pk)
    room = floor.rooms.all().order_by('room')
    context={
        'floor': floor,
        'room': room,
    }
    return render(request,'room.html',context)

@login_required(login_url='login')
def booking_room(request,pk):
    room = get_object_or_404(Room,id=pk)
    user_profile = request.user.userprofile
    booking = Booking.objects.filter(room=room)
    error_message = None
    # for handeling  the gender error
    if room.floor.hostel.gender != user_profile.gender:
        error_message = "Gender mismatch error."
        context={
            'user_profile': user_profile,
            'room':room,
            'error_message': error_message,
            'booking': booking,

        }
        return render(request, 'booking_room.html',context)
    # for handeling the error based on the user booking twice
    if Booking.objects.filter(user=user_profile.user).exists():
        error_message = "You cannot book a room more than twice "
        context={
            'room':room,
            'error_message': error_message,
            'booking': booking,

        }
        return render(request, 'booking_room.html',context)
    # for handling the error for the maximum capacity of the room
    if room.current_bookings >= room.max_capacity:
        error_message = "Maximum room capacity reached."
        context = {
            'room': room,
            'error_message': error_message,
            'booking': booking,
        }
        return render(request, 'booking_room.html', context)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit= False)
            booking.user = request.user
            booking.room = room
            booking.save()
            error_message = "Booking have been successfully done"
            context={
            'room':room,
            'error_message': error_message,
            'booking': booking,
            }
            return render(request, 'booking_room.html',context)

    else:
        form = BookingForm()
    context ={
        'form': form,
        'room': room,
        'error_message': error_message,
        'booking': booking,
    }
    return render (request,'booking_room.html', context)


# Menu web page view
@login_required(login_url='login')
def menu(request):
    menu = Menu.objects.all()
    context = {
        "menu":menu
    }
    return render(request,'menu.html',context)
# Review page to be seen for the particular hostel
@login_required(login_url='login')
def reviews(request, pk):
    hostel = get_object_or_404(Hostel,id=pk)
    review = hostel.reviews.all()
    context = {
        'hostel': hostel,
        'review': review,
    }
    return render(request,'reviews.html',context)

# Reviews page at the web page
@login_required(login_url='login')
def add_reviews(request, pk):
    hostel = get_object_or_404(Hostel, id=pk)
    user_profile = request.user.userprofile

    # for the opposite gender review problem
    if hostel.gender != user_profile.gender:
        error_message = "You cannot review more than twice "
        context={
            'hostel':hostel,
            'error_message': error_message,
        }
        return render(request,'review_form.html',context)

    # for handling the error based on the user reviewing twice
    if Review.objects.filter(user=user_profile.user).exists():
        error_message = "You cannot review more than twice "
        form = ReviewForm(request.POST)
        context={
            'hostel':hostel,
            'error_message': error_message,
            'form': form,

        }
        return render(request,'review_form.html',context)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.hostel = hostel
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'hostel': hostel,
    }
    return render(request, 'review_form.html', context)

# About us page for the web page
@login_required(login_url='login')
def help(request):
    captain = Counselor.objects.all()
    context = {
        'captain': captain
    }
    return render(request,'about_us.html',context)


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
        email = form.cleaned_data.get('email')
        reg_number = form.cleaned_data.get('reg_number')
        contact_no = form.cleaned_data.get('contact_no')
        gender = form.cleaned_data.get('gender')
        father_name = form.cleaned_data.get('father_name')
        father_email = form.cleaned_data.get('father_email')
        father_contact = form.cleaned_data.get('father_contact')
        mother_name = form.cleaned_data.get('mother_name')
        mother_email = form.cleaned_data.get('mother_email')
        mother_contact = form.cleaned_data.get('mother_contact')

        group = Group.objects.get(name='student')
        user.groups.add(group)
        Userprofile.objects.create(
            user=user,
            name=username,
            reg_number=reg_number,
            Email_address=email,
            contact_no=contact_no,
            gender=gender,
            Father_name=father_name,
            Father_email_address=father_email,
            Father_contact_no=father_contact,
            Mother_name=mother_name,
            Mother_email_address=mother_email,
            Mother_contact_no=mother_contact
        )
        return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

# User page
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def userpage(request):
    booking = Booking.objects.select_related('room__floor__hostel').filter(user=request.user).first()
    context ={
        'booking': booking,
        
    }
    return render(request,'admin_view/userpage.html',context)




#Dashboard for the admin view
@login_required(login_url='login')
@admin_only
def dashboard(request):
    user = Userprofile.objects.all().order_by('name')
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
#Hostel Details
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def hostel_detail(request,pk):
    hostel = get_object_or_404(Hostel, id=pk)
    floors = hostel.floors.prefetch_related(
        models.Prefetch('rooms', queryset=Room.objects.order_by('room'))
    ).order_by('number')

    context ={
        'hostel': hostel,
        'floor': floors,
    }
    return render(request,'admin_view/hostel_detail.html',context)
#Creating hostel
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
    return render(request, 'admin_view/Forms/hostel_form.html', context)
#Update hostel
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
    return render(request, 'admin_view/Forms/hostel_form.html', context)

#delete hostel
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
    return render(request,'admin_view/Forms/hostel_delete.html',context)

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
    return render(request,'admin_view/Forms/menu_form.html',context)
#  Menu update
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
    return render(request, 'admin_view/Forms/menu_form.html', context)
# Menu Delete
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
    return render(request,'admin_view/Forms/menu_delete.html',context)


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
    return render(request, 'admin_view/Forms/room_form.html', context)
# Update room
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_room(request,pk):
    room = get_object_or_404(Room, id=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('hostel_detail' ,pk=room.floor.hostel.id)  # Ensure this is the correct URL pattern name
    else:
        form = RoomForm(instance=room)
    
    context = {
        'form': form,
        'floor': room.floor,
    }
    return render(request, 'admin_view/Forms/room_form.html', context)
# delete room 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_room(request,pk):
    room = get_object_or_404(Room, id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('hostel_detail' ,pk=room.floor.hostel.id)
    context = {
        'room': room,
        'hostel': room.floor.hostel,
    }
    return render(request,'admin_view/Forms/room_delete.html',context)

# For the floor CRUD functions

#Create floor
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
    return render(request,'admin_view/Forms/floor_form.html',context)

# update floor
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_floor(request,pk):
    floor = get_object_or_404(Floor, id=pk)
    if request.method == 'POST':
        form = FloorForm(request.POST, request.FILES, instance=floor)
        if form.is_valid():
            form.save()
            return redirect('hostel_detail', pk=floor.hostel.id)  # Ensure this is the correct URL pattern name
    else:
        form = FloorForm(instance=floor)
    
    context = {
        'form': form,
        'hostel': floor.hostel,
    }
    return render(request, 'admin_view/Forms/floor_form.html', context)

# delete floor
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_floor(request,pk):
    floor = get_object_or_404(Floor, id=pk)
    if request.method == 'POST':
        floor.delete()
        return redirect('hostel_detail', pk= floor.hostel.id)
    context = {
        'floor': floor
    }
    return render(request,'admin_view/Forms/floor_delete.html',context)

# For the booking view at the admin page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def booking_admin(request):
    hostel = Hostel.objects.all()
    context = {
        'hostel': hostel,
    }
    return render(request, 'admin_view/booking.html',context)

#booking details

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
#delete booking

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
    return render(request,'admin_view/Forms/booking_delete.html',context)

# Help page in the admin view
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def help_admin(request):
    counselor= Counselor.objects.all()
    context = {
        'counselor': counselor,
    }
    return render(request,'admin_view/counselor.html',context)
# Create Counselor
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_counselor(request):
    form = CounselorForm
    if request.method == 'POST':
        form = CounselorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('counselor')  # Ensure this is the correct URL pattern name
    else:
        form = CounselorForm()
    context = {
        'form': form
    }
    return render(request,'admin_view/Forms/counselor_form.html',context)

# Delete Counselor
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_counselor(request, pk):
    counselor = get_object_or_404(Counselor, id=pk)
    if request.method == 'POST':
        counselor.delete()
        return redirect('counselor')  # Ensure this is the correct URL pattern name
    context = {
        'counselor': counselor
    }
    return render(request, 'admin_view/Forms/counselor_confirm_delete.html', context)

# Update_counselor
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_counselor(request, pk):
    counselor = get_object_or_404(Counselor, id=pk)
    form = CounselorForm(instance=counselor)
    if request.method == 'POST':
        form = CounselorForm(request.POST, request.FILES, instance=counselor)
        if form.is_valid():
            form.save()
            return redirect('counselor')  # Ensure this is the correct URL pattern name
    context = {
        'form': form,
        'counselor': counselor
    }
    return render(request, 'admin_view/Forms/counselor_form.html', context)

# For the review handling by the admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def review_admin(request):
    review = Review.objects.all()
    context = {
        'review': review,

    }
    return render(request,'admin_view/reviews.html',context)
#For deleting the reviews
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_admin')  # Ensure this is the correct URL pattern name
    context = {
        'review': review,
    }
    return render(request, 'admin_view/Forms/review_delete.html', context)





    

    

    
    


