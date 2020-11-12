from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


def get_user_by_email(email):
    """
    get user by email or by secondary email
    raise ObjectDoesNotExist
    """
    try:
        user = User._default_manager.get(**{User.EMAIL_FIELD: email})
        return user
    except ObjectDoesNotExist:
        return None