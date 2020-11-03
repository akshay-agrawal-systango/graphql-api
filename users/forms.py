from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ('password', 'date_joined')