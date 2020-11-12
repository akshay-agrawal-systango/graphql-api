from django.db import models
from django.contrib.auth.models import User
from .utils import get_token, get_token_paylod
from django.contrib.sites.shortcuts import get_current_site
import time
from django.template.loader import render_to_string
from .constants import Messages, TokenAction
from .exceptions import UserAlreadyVerified
from .signals import user_verified

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "%s email confirmed : %s" % (self.user, self.email_confirmed)

    def get_email_context(self, info, action, **kwargs):
        token = get_token(self.user, action, **kwargs)
        site = get_current_site(info.context)
        return {
            "user": self.user,
            "request": info.context,
            "token": token,
            "port": info.context.get_port(),
            "site_name": site.name,
            "domain": site.domain,
            "protocol": "https" if info.context.is_secure() else "http",
            "timestamp": time.time(),
        }

    def send_activation_email(self, info, *args, **kwargs):
        email_context = self.get_email_context(info, TokenAction.ACTIVATION)
        subject = 'Activate Your Account'
        message = render_to_string('account_activation_email.html', email_context)
        return self.user.email_user(subject, message)

    def send_password_reset_email(self, info, *args, **kwargs):
        email_context = self.get_email_context(info, TokenAction.PASSWORD_RESET)
        subject = 'Reset Your Account Password'
        message = render_to_string('reset_password_email.html', email_context)
        return self.user.email_user(subject, message)

    @classmethod
    def verify(cls, token):
        payload = get_token_paylod(token, TokenAction.ACTIVATION)
        user = User._default_manager.get(**payload)
        profile = cls.objects.get(user=user)
        if profile.email_confirmed is False:
            profile.email_confirmed = True
            profile.save(update_fields=["email_confirmed"])
            user_verified.send(sender=cls, user=user)
        else:
            raise UserAlreadyVerified

    @classmethod
    def email_is_free(cls, email):
        try:
            User._default_manager.get(**{User.EMAIL_FIELD: email})
            return False
        except Exception:
            pass
        return True

    @classmethod
    def clean_email(cls, email=False):
        if email:
            if cls.email_is_free(email) is False:
                raise EmailAlreadyInUse

