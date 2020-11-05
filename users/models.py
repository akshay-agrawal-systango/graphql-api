from django.db import models
from django.contrib.auth.models import User
from .utils import get_token, get_token_paylod
from .exceptions import UserAlreadyVerified

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    profession = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return "%s - status" % (self.user)

    def get_email_context(self, info, **kwargs):
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
        email_context = self.get_email_context(info)
        subject = 'Activate Your Account'
        message = render_to_string('account_activation_email.html', email_context)
        return self.user.email_user(subject, message)

    def send_password_set_email(self, info, *args, **kwargs):
        email_context = self.get_email_context(info)
        subject = 'Reset Your Account Password'
        message = render_to_string('reset_password_email.html', email_context)
        return self.user.email_user(subject, message)

    @classmethod
    def verify(cls, token):
        payload = get_token_paylod(token)
        user = UserModel._default_manager.get(**payload)
        profile = cls.objects.get(user=user)
        if profile.email_confirmed is False:
            profile.email_confirmed = True
            profile.save()
        else:
            raise UserAlreadyVerified
