from django.contrib import admin

# Register your models here.
from .models import Hostel, Hostel_description,Menu

class MyModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Specifies the fields to display in the list view
    search_fields = ['title']  # Adds a search box that searches the 'title' field

class Hostel_description_line(admin.StackedInline):
    model =  Hostel_description
    extra = 1

class Hostel_admin(admin.ModelAdmin):
    inlines = [Hostel_description_line,]

# Register your models here.
admin.site.register(Hostel,Hostel_admin)
admin.site.register(Menu)