
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
]