import graphene
from .types import UserType
from .mutations import CreateUserMutation, RegisterUserMutation, ResetPasswordEmailMutation
from django.contrib.auth import get_user_model


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_users(self, info, **kwargs):
        User = get_user_model()
        return User.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    register_user = RegisterUserMutation.Field()
    reset_password = ResetPasswordEmailMutation.Field()

