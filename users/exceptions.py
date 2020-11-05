from django.utils.translation import gettext as _


class GraphQLAuthError(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class UserAlreadyVerified(GraphQLAuthError):
    default_message = _("User already verified.")

class TokenScopeError(GraphQLAuthError):
    default_message = _("This token if for something else.")

