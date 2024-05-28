from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Hostel,Menu,Room,Floor,Booking,Review,Counselor
from django import forms
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    reg_number = forms.IntegerField(required=True)
    contact_no = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    father_name = forms.CharField(max_length=200)
    father_email = forms.EmailField(required=True)
    father_contact = forms.IntegerField(required=True)
    mother_name = forms.CharField(max_length=200)
    mother_email = forms.EmailField(required=True)
    mother_contact = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'reg_number', 'contact_no', 'gender', 'father_name', 'father_email', 'father_contact', 'mother_name', 'mother_email', 'mother_contact']

class HostelForm(ModelForm):
    class Meta:
        model = Hostel
        fields = '__all__'

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields= '__all__'

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields= ['id','room', 'status', 'max_capacity']

class FloorForm(ModelForm):
    class Meta:
        model = Floor
        fields = ['number']

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['check_in'].required = False
        self.fields['check_out'].required = False

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'reviews']
        widgets = {
            'reviews': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
        }
class CounselorForm(ModelForm):
    class Meta:
        model = Counselor
        fields = '__all__'


