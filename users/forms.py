from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile 

# class SignUpForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = '__all__'
#         exclude = ('password', 'date_joined')


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')