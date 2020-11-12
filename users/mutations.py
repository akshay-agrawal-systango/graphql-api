import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation, DjangoModelFormMutation
# from .forms import SignUpForm, ProfileForm
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
from .bases import MutationMixin, DynamicArgsMixin
from .mixins import (
    RegisterMixin,
    VerifyAccountMixin,
    PasswordResetMixin,
    UpdateAccountMixin,
    SendPasswordResetEmailMixin,
    PasswordChangeMixin,
    EmailChangeMixin,
    )


# class CreateUserMutation(DjangoFormMutation):
    
#     class Meta:
#         form_class = SignUpForm


# class RegisterUserMutation(graphene.Mutation):
#     user = graphene.Field(UserType)

#     class Arguments:
#         username = graphene.String(required=True)
#         password = graphene.String(required=True)
#         email = graphene.String(required=True)

#     def mutate(self, info, username, password, email):
#         users = User.objects.filter(Q(username=username)|Q(email=email))
#         if users:
#             raise Exception('Email or username already exits')
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             profile = Profile.objects.create(user=user)

#             # send account activation email
#             current_site = get_current_site(info.context)
#             subject = 'Activate Your Account'
#             message = render_to_string('account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': token_generator.make_token(user),
#             })
#             user.email_user(subject, message)

#         return RegisterUserMutation(user=user)


# class ResetPasswordEmailMutation(graphene.Mutation):
#     user = graphene.Field(UserType)

#     class Arguments:
#         email = graphene.String(required=True)

#     def mutate(self, info, email):
#         user = User.objects.filter(email=email).first()
#         # send email to reset password
#         if user:
#             current_site = get_current_site(info.context)
#             subject = 'Reset Your Account Password'
#             message = render_to_string('reset_password_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': token_generator.make_token(user),
#             })
#             user.email_user(subject, message)
#         else:
#             raise Exception('User does not exits!')

#         return ResetPasswordEmailMutation(user=user)


# class RegisterUser(graphene.Mutation):

#     user = graphene.Field(UserType)

#     class Arguments:
#         username = graphene.String(required=True)
#         password = graphene.String(required=True)
#         email = graphene.String(required=True)

#     def mutate(self, info, username, password, email):
#         users = User.objects.filter(Q(username=username)|Q(email=email))
#         if users:
#             raise Exception('Email or username already exits')
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             profile = Profile.objects.create(user=user)
#             profile.send_activation_email(info)

#         return RegisterUser(user=user)

# class VerifyEmail(graphene.Mutation):

#     user = graphene.Field(UserType)

#     class Arguments:
#         token = graphene.String(required=True)

#     def mutate(self, info, token):
#         try:
#             user = Profile.verify(token)
#             return VerifyEmail(user=user)
#         except:
#             raise Exception('Invalid token')


# class ResetPasswordEmail(graphene.Mutation):
#     user = graphene.Field(UserType)

#     class Arguments:
#         email = graphene.String(required=True)

#     def mutate(self, info, email):
#         user = User.objects.filter(email=email).first()
#         # send email to reset password
#         if user:
#             user.profile.send_password_reset_email(info)
#         else:
#             raise Exception('User does not exits!')

#         return ResetPasswordEmail(user=user)


# class SetPassword(graphene.Mutation):
#     user = graphene.Field(UserType)

#     class Arguments:
#         token = graphene.String(required=True)
#         new_password = graphene.String(required=True)

#     def mutate(self, info, token, new_password):
#         try:
#             user = Profile.verify(token)
#             user.set_password(new_password)
#             user.save()
#             return ResetPasswordEmail(user=user)
#         except:
#             raise Exception('Invalid token')


# class UpdateProfile(DjangoModelFormMutation):

#     class Meta:
#         form_class = ProfileForm


class Register(MutationMixin, DynamicArgsMixin, RegisterMixin, graphene.Mutation):

    __doc__ = RegisterMixin.__doc__

    _required_args = ["username", "email", "password1", "password2"]


class VerifyAccount(
    MutationMixin, DynamicArgsMixin, VerifyAccountMixin, graphene.Mutation
):
    __doc__ = VerifyAccountMixin.__doc__
    _required_args = ["token"]


class SendPasswordResetEmail(
    MutationMixin, DynamicArgsMixin, SendPasswordResetEmailMixin, graphene.Mutation
):
    __doc__ = SendPasswordResetEmailMixin.__doc__
    _required_args = ["email"]


class PasswordReset(
    MutationMixin, DynamicArgsMixin, PasswordResetMixin, graphene.Mutation
):
    __doc__ = PasswordResetMixin.__doc__
    _required_args = ["token", "new_password1", "new_password2"]


class UpdateAccount(
    MutationMixin, DynamicArgsMixin, UpdateAccountMixin, graphene.Mutation
):
    __doc__ = UpdateAccountMixin.__doc__
    _args = ["first_name", "last_name"]


class PasswordChange(
    MutationMixin, PasswordChangeMixin, DynamicArgsMixin, graphene.Mutation
):
    __doc__ = PasswordChangeMixin.__doc__
    _required_args = ["old_password", "new_password1", "new_password2"]


class EmailChange(
    MutationMixin, EmailChangeMixin, DynamicArgsMixin, graphene.Mutation
):
    __doc__ = PasswordChangeMixin.__doc__
    _required_args = ["email"]