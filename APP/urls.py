
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
    path('dash/',views.dashboard,name='dash'),
    path('student/<str:pk_test>/', views.student_profile, name='student'),
    path('hostel/',views.hostel_admin_view,name='hostel'),
    path('hostel_create/',views.create_hostel,name='hostel_create'),
    path('menu_admin/',views.menu_admin,name='menu_admin'),
    path('menu_create/',views.menu_create,name='menu_create'),
    path('hostel_update/<str:pk>/',views.update_hostel,name='hostel_update'),
    path('hostel_delete/<str:pk>/',views.delete_hostel,name='hostel_delete'),
    path('menu_update/<str:pk>/',views.menu_update,name='menu_update'),
    path('menu_delete/<str:pk>/',views.menu_delete,name='menu_delete'),
    path('hostel_detail/<str:pk>/',views.hostel_detail,name='hostel_detail'),
    path('create_room/', views.create_room, name='create_room'),
    path('room_update/<str:pk>/',views.update_room,name='room_update'),
    path('room_delete/<str:pk>/',views.delete_room,name='room_delete'),
    path('create_floor/', views.create_floor, name='create_floor'),
    path('floor_update/<str:pk>/',views.update_floor,name='floor_update'),
    path('floor_delete/<str:pk>/',views.delete_floor,name='floor_delete'),
    path('booking_admin/',views.booking_admin, name='booking_admin'),
    path('booking_detail/<str:pk>',views.booking_detail, name='booking_detail'),
    path('delete_booking/<str:pk>/',views.delete_booking,name='delete_booking'),
]