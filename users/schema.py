import graphene
from .types import UserType, ProfileType
# from .mutations import (
#     CreateUserMutation,
#     RegisterUserMutation,
#     ResetPasswordEmailMutation,
#     RegisterUser,
#     VerifyEmail,
#     ResetPasswordEmail,
#     SetPassword,
#     UpdateProfile,
#     )
from .mutations import (
    Register,
    VerifyAccount,
    SendPasswordResetEmail,
    PasswordReset,
    UpdateAccount,
    PasswordChange,
    EmailChange,
    )
from django.contrib.auth.models import User
from .models import Profile
from graphene_django.filter.fields import DjangoFilterConnectionField

class Query(graphene.ObjectType):
    # hello query to check is_authenticated or not
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    user_by_id = graphene.Field(UserType, id=graphene.Int())
    profile_by_id = graphene.Field(ProfileType, id=graphene.Int())
    users = DjangoFilterConnectionField(UserType)
    profiles = DjangoFilterConnectionField(ProfileType)

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        is_authenticated = info.context.user.is_authenticated 
        return f'Hello {name} you are logged in : {is_authenticated}'

    def resolve_user_by_id(root, info, id):
        return User.objects.get(id=id)

    def resolve_profile_by_id(root, info, id):
        return Profile.objects.get(id=id)

class Mutation(graphene.ObjectType):
    # create_user = CreateUserMutation.Field()
    # register_user = RegisterUserMutation.Field()
    # reset_password = ResetPasswordEmailMutation.Field()
    # register_user = RegisterUser.Field()
    # verify_email = VerifyEmail.Field()
    # reset_password_email = ResetPasswordEmail.Field()
    # set_password = SetPassword.Field()
    # update_profile = UpdateProfile.Field()
    register_user = Register.Field()
    verify_account = VerifyAccount.Field()
    send_password_reset_email = SendPasswordResetEmail.Field()
    password_reset = PasswordReset.Field()
    update_account = UpdateAccount.Field()
    password_change = PasswordChange.Field()
    email_change = EmailChange.Field()

