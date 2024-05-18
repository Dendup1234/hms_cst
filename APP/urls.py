
from django.urls import path
from . import views

urlpatterns = [
    path('',views.hostel, name='home'),
    path('menu/',views.menu, name='menu'),
    path('Review',views.reviews, name='reviews'),
    path('about',views.aboutus,name='about'),
]