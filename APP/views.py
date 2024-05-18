from django.shortcuts import render

# Create your views here.
from .models import Hostel,Menu
# Create your views here.

def hostel(request):
    hostel = Hostel.objects.all()
    context = {
        "hostel": hostel
    }
    return render(request,'index.html',context)

def menu(request):
    menu = Menu.objects.all()
    context = {
        "menu":menu
    }
    return render(request,'menu.html',context)
def reviews(request):
    return render(request,'Review.html')

def aboutus(request):
    return render(request,'about_us.html')