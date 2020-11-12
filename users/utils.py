from django.core import signing
from .exceptions import TokenScopeError


def get_token(user, action, **kwargs):
    username = user.get_username()
    if hasattr(username, "pk"):
        username = username.pk
    payload = {user.USERNAME_FIELD: username, "action": action}
    if kwargs:
        payload.update(**kwargs)
    token = signing.dumps(payload)
    return token


def get_token_paylod(token, action, exp=None):
    # import pdb;pdb.set_trace();
    payload = signing.loads(token, max_age=exp)
    _action = payload.pop("action")
    if _action != action:
        raise TokenScopeError
    return payload

def revoke_user_refresh_token(user):
    refresh_tokens = user.refresh_tokens.all()
    for refresh_token in refresh_tokens:
        try:
            refresh_token.revoke()
        except Exception:  # JSONWebTokenError
            pass