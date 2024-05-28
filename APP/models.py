from django.db import models
from django.contrib.auth.models import User

# For the user
class Userprofile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE,related_name='userprofile')
    name = models.CharField(max_length=200,null=True)
    reg_number = models.IntegerField(default=0,null=True,unique=True)
    Email_address = models.CharField(max_length=100, null=True)
    contact_no = models.IntegerField(default=0,null=True)
    gender = (
        ('M','Male'),
        ('F','Female'),
    )
    gender = models.CharField(max_length=200,null=True,choices= gender)
    Father_name = models.CharField(max_length=200,null=True)
    Father_email_address = models.CharField(max_length=200,null=True)
    Father_contact_no = models.IntegerField(default=0,null= True)
    Mother_name = models.CharField(max_length=200,null= True)
    Mother_email_address = models.CharField(max_length=200,null = True)
    Mother_contact_no = models.IntegerField(default= 0, null = True)


    def __str__ (self):
        return self.name if self.name else self.user.username if self.user else "Unnamed Profile"
    
# Hostel   
class Hostel(models.Model):
    gender = (
        ('M','Male'),
        ('F','Female'),
    )
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200,null= True,choices=gender)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='hostels/')

    def __str__ (self):
        return self.name

# Menu
class Menu(models.Model): 
    day = models.CharField(max_length=200)
    breakfast_description = models.CharField(max_length=200)
    breakfast_image = models.ImageField(upload_to='breakfasts/')  # Adjusted upload_to path
    lunch_description = models.CharField(max_length=200)
    lunch_image = models.ImageField(upload_to='lunches/')  # Adjusted upload_to path
    dinner_description = models.CharField(max_length=200)
    dinner_image = models.ImageField(upload_to='dinners/')  # Adjusted upload_to path

    def __str__(self):
        return self.day  # Fixed to return the string representation of day

# Floor of the hostel
class Floor(models.Model):
    hostel = models.ForeignKey(Hostel,related_name='floors',null=True,on_delete=models.SET_NULL)
    number = models.IntegerField(default=0,null=True)

    def __str__(self):
        return f"{self.hostel.name} Floor - {self.number}"

# Room
class Room (models.Model):
    Status = (
        ('Vacant','Vacant'),
        ('Full','Full'),
        ('Maintainece','Maintainece')
    )
    floor = models.ForeignKey(Floor,related_name='rooms' ,null=True,on_delete=models.SET_NULL)
    room = models.CharField(max_length=200)
    max_capacity = models.IntegerField(default=3)
    current_bookings = models.IntegerField(default=0)
    status = models.CharField(max_length=200,choices=Status ,default='Vacant')

    def __str__ (self):
        return f"{self.room}-{self.status}"
    
    def update_status(self):
        if self.current_bookings >= self.max_capacity:
            self.status = 'Full'
        elif self.status == 'Full':
            self.status = 'Vacant'  # Assuming you want to change back to Vacant if capacity is no longer full
        self.save()
    
import datetime

def get_end_of_semester():
    # Replace this with the actual logic to determine the end of the semester
    return datetime.date(datetime.datetime.now().year, 6, 7)

#Booking
class Booking(models.Model):
    user = models.OneToOneField(User, null=True, related_name='booking', on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, null = True, on_delete=models.SET_NULL)
    check_in = models.DateField(default=datetime.date.today,blank = True)
    check_out = models.DateField(default=get_end_of_semester,blank = True)

    def __str__(self):
        return f"{self.user} has booked {self.room}"
    # logic when the room is full when reached the maximum capacity
    def save(self, *args, **kwargs):
        if self.room.status != 'Full':
            self.room.current_bookings += 1
            self.room.update_status()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Room is full")
    # for the delete concept
    def delete(self, *args, **kwargs):
        room = self.room
        super().delete(*args, **kwargs)
        if room.booking_set.count() == 0:
            room.current_bookings = 0
        else:
            room.current_bookings = room.booking_set.count()
        room.update_status()
        room.save()
# Reviews
class Review(models.Model):
    hostel = models.ForeignKey(Hostel,related_name='reviews',on_delete= models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    comment = models.TextField()
    reviews = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username}:Reviewed {self.hostel.name}'

class Counselor(models.Model):
    name = models.CharField(max_length=200)
    block = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='counselors/')

    def __str__(self):
        return self.name
    


    