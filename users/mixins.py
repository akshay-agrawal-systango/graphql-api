from django.contrib.auth.forms import SetPasswordForm
from .utils import revoke_user_refresh_token, get_token_paylod
from django.contrib.auth.models import User
from .constants import Messages, TokenAction
from django.core.signing import BadSignature, SignatureExpired
from .exceptions import TokenScopeError, UserAlreadyVerified, UserNotVerified, EmailAlreadyInUse
from .bases import Output
from .forms import UpdateAccountForm, EmailForm, RegisterForm
from .decorators import verification_required
from .shortcuts import get_user_by_email
from django.core.exceptions import ObjectDoesNotExist
from .signals import user_registered
from django.db import transaction
import graphene
from .models import Profile


class RegisterMixin(Output):
    """
    Register new user (username, email, password)

    When creating the user, it also creates a `Profile`
    related to that user, making it possible to track
    if the user email is verified.

    Send account verification email.
    """

    form = RegisterForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            with transaction.atomic():
                f = cls.form(kwargs)
                if f.is_valid():
                    email = kwargs.get(User.EMAIL_FIELD, False)
                    Profile.clean_email(email)
                    user = f.save()
                    user.profile.send_activation_email(info)
                    user_registered.send(sender=cls, user=user)
                    return cls(success=True)
                else:
                    return cls(success=False, errors=f.errors.get_json_data())
        except EmailAlreadyInUse:
            return cls(
                success=False,
                errors={User.EMAIL_FIELD: Messages.EMAIL_IN_USE},
            )


class VerifyAccountMixin(Output):
    """
    Verify user account.

    Receive the token that was sent by email.
    If the token is valid, make the user verified
    by making the `user.profile.email_confirmed` field true.
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            token = kwargs.get("token")
            Profile.verify(token)
            return cls(success=True)
        except UserAlreadyVerified:
            return cls(success=False, errors=Messages.ALREADY_VERIFIED)
        except SignatureExpired:
            return cls(success=False, errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)


class SendPasswordResetEmailMixin(Output):
    """
    Send password reset email.

    For non verified users, send an activation
    email instead.

    Accepts both primary and secondary email.

    If there is no user with the requested email,
    a successful response is returned.
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            email = kwargs.get("email")
            f = EmailForm({"email": email})
            if f.is_valid():
                user = get_user_by_email(email)
                user.profile.send_password_reset_email(info)
                return cls(success=True)
            return cls(success=False, errors=f.errors.get_json_data())
        except ObjectDoesNotExist:
            return cls(success=True)
        except UserNotVerified:
            user = get_user_by_email(email)
            user.profile.send_activation_email(info)
            return cls(
                success=False,
                errors={"email": Messages.NOT_VERIFIED_PASSWORD_RESET},
            )


class PasswordResetMixin(Output):
    """
    Change user password without old password.

    Receive the token that was sent by email.

    If token and new passwords are valid, update
    user password and in case of using refresh
    tokens, revoke all of them.

    Also, if user has not been verified yet, verify it.
    """

    form = SetPasswordForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            token = kwargs.pop("token")
            payload = get_token_paylod(token, TokenAction.PASSWORD_RESET)
            user = User._default_manager.get(**payload)
            f = cls.form(user, kwargs)
            if f.is_valid():
                revoke_user_refresh_token(user)
                user = f.save()
                if user.profile.email_confirmed is False:
                    user.profile.email_confirmed = True
                    user.profile.save(update_fields=["email_confirmed"])
                return cls(success=True)
            return cls(success=False, errors=f.errors.get_json_data())
        except SignatureExpired:
            return cls(success=False, errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)


class UpdateAccountMixin(Output):
    """
    Update user model fields.

    User must be verified.
    """

    form = UpdateAccountForm

    @classmethod
    @verification_required
    def resolve_mutation(cls, root, info, **kwargs):
        user = info.context.user
        f = cls.form(kwargs, instance=user)
        if f.is_valid():
            f.save()
            return cls(success=True)
        else:
            return cls(success=False, errors=f.errors.get_json_data())