import graphene
from .types import UserType, ProfileType
from .mutations import (
    CreateUserMutation,
    RegisterUserMutation,
    ResetPasswordEmailMutation,
    RegisterUser,
    VerifyEmail,
    ResetPasswordEmail,
    SetPassword,
    UpdateProfile
    )
from django.contrib.auth.models import User
from .models import Profile
from graphene_django.filter.fields import DjangoFilterConnectionField

class Query(graphene.ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    goodbye = graphene.String()
    user_by_id = graphene.Field(UserType, id=graphene.Int())
    profile_by_id = graphene.Field(ProfileType, id=graphene.Int())
    users = DjangoFilterConnectionField(UserType)
    profile = DjangoFilterConnectionField(ProfileType)

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        is_verified = info.context.user.is_authenticated 
        return f'Hello {name} you are logged in : {is_verified}'

    def resolve_goodbye(root, info):
        return 'See ya!'

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user_by_id(root, info, id):
        return User.objects.get(id=id)

    def resolve_profile_by_id(root, info, id):
        return Profile.objects.get(id=id)

class Mutation(graphene.ObjectType):
    # create_user = CreateUserMutation.Field()
    # register_user = RegisterUserMutation.Field()
    # reset_password = ResetPasswordEmailMutation.Field()
    register_user = RegisterUser.Field()
    verify_email = VerifyEmail.Field()
    reset_password_email = ResetPasswordEmail.Field()
    set_password = SetPassword.Field()
    # to update profile user_id and profile_id is required in mutaion query
    update_profile = UpdateProfile.Field()

