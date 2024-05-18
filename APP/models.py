from django.db import models
from django.contrib.auth.models import AbstractUser

# for the User Registeration

# Create your models here.
class Hostel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='hostels/')

    def __str__ (self):
        return self.name
class Hostel_description(models.Model):
    hostel = models.ForeignKey(Hostel ,related_name="feature",on_delete=models.CASCADE,null=True)
    feature = models.TextField()    
    def __str__ (self):
        return self.feature

class Menu(models.Model):  # Class names should be capitalized
    day = models.CharField(max_length=200)
    breakfast_description = models.CharField(max_length=200)
    breakfast_image = models.ImageField(upload_to='breakfasts/')  # Adjusted upload_to path
    lunch_description = models.CharField(max_length=200)
    lunch_image = models.ImageField(upload_to='lunches/')  # Adjusted upload_to path
    dinner_description = models.CharField(max_length=200)
    dinner_image = models.ImageField(upload_to='dinners/')  # Adjusted upload_to path

    def __str__(self):
        return self.day  # Fixed to return the string representation of day
    