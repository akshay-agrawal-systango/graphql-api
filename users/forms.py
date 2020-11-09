from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile 

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ('password', 'date_joined')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
