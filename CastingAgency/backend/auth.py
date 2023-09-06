import json, sys, os
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from dotenv import load_dotenv
from urllib.request import urlopen

# -----------------------------------------------------------------------------------------------!
# Login/Signup Domain details
# Domain details stored in .env file
# -----------------------------------------------------------------------------------------------!
load_dotenv()
AUTH0_DOMAIN = os.getenv("auth0_domain")
ALGORITHMS = os.getenv("algorithms")
API_AUDIENCE = os.getenv("api_audience")


# -----------------------------------------------------------------------------------------------!
# AuthError Exception
# A standardized way to communicate auth failure modes
# -----------------------------------------------------------------------------------------------!
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# -----------------------------------------------------------------------------------------------!
# Auth Header
# -----------------------------------------------------------------------------------------------!
def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )
    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid header",
                "description": "Authorization header must start with Bearer.",
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found"}, 401
        )
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be bearer token",
            },
            401,
        )

    token = parts[1]
    return token


# -----------------------------------------------------------------------------------------------!
# check_permissions(permission, payload) method
# -----------------------------------------------------------------------------------------------!
def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError(
            {"success": False, "error": 400, "message": "Permissions not in payload"},
            400,
        )

    if permission not in payload["permissions"]:
        raise AuthError({"success": False, "error": 403, "message": "Forbidden"}, 403)

    return True


# -----------------------------------------------------------------------------------------------!
# verify_decode_jwt(token) method
# -----------------------------------------------------------------------------------------------!
def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError(
            {"code": "invalid_header", "description": "Authorization malformed."}, 401
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",  # type: ignore
            )
            return payload

        except jwt.ExpiredSignatureError:  # type: ignore
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."}, 401
            )

        except jwt.JWTClaimsError:  # type: ignore
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, check the audience and issuer",
                },
                401,
            )
        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            )
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


# -----------------------------------------------------------------------------------------------!
# @requires_auth(permission) decorator method
# -----------------------------------------------------------------------------------------------!
def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
