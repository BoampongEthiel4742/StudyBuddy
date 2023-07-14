from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


 
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['host', 'name', 'topic', 'description']



class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','full_name', 'username', 'email', 'password']