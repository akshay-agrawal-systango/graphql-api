import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from .forms import SignUpForm
from django.contrib.auth.models import User
from .types import UserType
from django.db.models import Q
from django.core.mail import send_mail
from .tokens import token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import Profile


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
            profile = Profile.objects.create(user=user)

            # send account activation email
            current_site = get_current_site(info.context)
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })
            user.email_user(subject, message)

        return RegisterUserMutation(user=user)


class ResetPasswordEmailMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        user = User.objects.filter(email=email).first()
        # send email to reset password
        if user:
            current_site = get_current_site(info.context)
            subject = 'Reset Your Account Password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })
            user.email_user(subject, message)
        else:
            raise Exception('User does not exits!')

        return ResetPasswordEmailMutation(user=user)


class SetPasswordMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=True)

    def mutate(self, info):
        pass