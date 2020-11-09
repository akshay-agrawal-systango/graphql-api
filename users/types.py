from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from .models import Profile
import graphene


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = '__all__'
        interfaces = (graphene.relay.Node,)

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = '__all__'
        interfaces = (graphene.relay.Node,)


import graphene
from graphene_django.utils import camelize

from .exceptions import WrongUsage


class ExpectedErrorType(graphene.Scalar):
    class Meta:
        description = """
    Errors messages and codes mapped to
    fields or non fields errors.
    Example:
    {
        field_name: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        other_field: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        nonFieldErrors: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ]
    }
    """

    @staticmethod
    def serialize(errors):
        if isinstance(errors, dict):
            if errors.get("__all__", False):
                errors["non_field_errors"] = errors.pop("__all__")
            return camelize(errors)
        elif isinstance(errors, list):
            return {"nonFieldErrors": errors}
        raise WrongUsage("`errors` must be list or dict!")