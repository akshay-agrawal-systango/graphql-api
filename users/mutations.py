import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from .forms import SignUpForm


class CreateUserMutation(DjangoFormMutation):
    
    class Meta:
        form_class = SignUpForm

