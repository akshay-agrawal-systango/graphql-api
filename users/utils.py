from django.core import signing


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
    payload = signing.loads(token, max_age=exp)
    _action = payload.pop("action")
    if _action != action:
        raise Exception('Invalid token')
    return payload