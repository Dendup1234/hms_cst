from django.db import models

# For the user
class User(models.Model):
    name = models.CharField(max_length=200,null=True)
    reg_number = models.IntegerField(default=0,null=True)
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
        return self.name
    
    
class Hostel(models.Model):
    id = models.IntegerField(default=0,primary_key=True)
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

class Menu(models.Model):  # Class names should be capitalized
    id = models.IntegerField(default=0,primary_key=True)
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

class Room (models.Model):
    id = models.IntegerField(default=0,primary_key=True)
    Status = (
        ('Vacant','Vacant'),
        ('Full','Full'),
        ('Maintainece','Maintainece')
    )
    floor = models.ForeignKey(Floor,related_name='rooms' ,null=True,on_delete=models.SET_NULL)
    room = models.CharField(max_length=200)
    max_capacity = models.IntegerField(default=1)
    current_bookings = models.IntegerField(default=0)
    status = models.CharField(max_length=200,choices=Status)

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

class Booking(models.Model):
    user = models.ForeignKey(User, null= True ,on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, null = True, on_delete=models.SET_NULL)
    check_in = models.DateField(default=datetime.date.today)
    check_out = models.DateField(default=get_end_of_semester)

    def __str__(self):
        return f"{self.user} has booked {self.room}"
    
    def save(self, *args, **kwargs):
        if self.room.status != 'Full':
            self.room.current_bookings += 1
            self.room.update_status()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Room is full")


    