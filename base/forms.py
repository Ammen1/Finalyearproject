from django.forms import ModelForm
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from account.models import  Customer
from .models import Room


class MyUserCreationForm(BaseUserManager):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = Customer
        fields = [ 'name', 'email']
