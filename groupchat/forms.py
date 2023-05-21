from django.forms import ModelForm

from .models import Room
from account.models import Customer




class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['avatar', 'name', 'email', 'bio']
