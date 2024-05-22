from django.contrib import admin

# Register your models here.
from .models import Hostel,Menu,User,Room,Booking,Floor

class MyModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Specifies the fields to display in the list view
    search_fields = ['title']  # Adds a search box that searches the 'title' field



# Register your models here.
admin.site.register(Hostel)
admin.site.register(Menu)
admin.site.register(Room)
admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Floor)