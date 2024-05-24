from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Hostel,Menu,Room,Floor

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

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


