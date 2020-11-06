import graphene
from .types import UserType
from .mutations import (
    CreateUserMutation,
    RegisterUserMutation,
    ResetPasswordEmailMutation,
    RegisterUser,
    VerifyEmail,
    ResetPasswordEmail,
    SetPassword
    )
from django.contrib.auth import get_user_model


class Query(graphene.ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    goodbye = graphene.String()
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

    def resolve_users(self, info, **kwargs):
        User = get_user_model()
        return User.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

class Mutation(graphene.ObjectType):
    # create_user = CreateUserMutation.Field()
    # register_user = RegisterUserMutation.Field()
    # reset_password = ResetPasswordEmailMutation.Field()
    register_user = RegisterUser.Field()
    verify_email = VerifyEmail.Field()
    reset_password = ResetPasswordEmail.Field()
    set_password = SetPassword.Field()

