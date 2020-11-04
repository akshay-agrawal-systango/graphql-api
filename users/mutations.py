import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from .forms import SignUpForm
from django.contrib.auth.models import User
from .types import UserType
from django.db.models import Q
from django.core.mail import send_mail


class CreateUserMutation(DjangoFormMutation):
    
    class Meta:
        form_class = SignUpForm


class RegisterUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        users = User.objects.filter(Q(username=username)|Q(email=email))
        if users:
            raise Exception('Email or username already exits')
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            # send email

        return RegisterUserMutation(user=user)


class ResetPasswordEmailMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        user = User.objects.get(email=email)
        # send email

        return ResetPasswordEmailMutation(user=user)
