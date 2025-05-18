from functools import wraps
from flask import request, abort

# Simple token-based auth for demo purposes
USERS = {
    "admin": "secret-token",
}

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token not in USERS.values():
            abort(401)
        return f(*args, **kwargs)
    return wrapper
