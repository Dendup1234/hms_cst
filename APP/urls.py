
from django.urls import path
from . import views

urlpatterns = [
    path('',views.hostel, name='home'),
    path('menu/',views.menu, name='menu'),
    path('Review/',views.reviews, name='reviews'),
    path('about/',views.aboutus,name='about'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.register,name='register'),
]