import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-8bzdf01x.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    # retrieve auth header from request recieved
    auth_header = request.headers.get('Authorization', None)
    # check if request contains authorization header 
    if not auth_header:
        raise AuthError({
        'code': 'Auth Header missing',
        'description': 'Authorization header must be provided'
    }, 401)
    # split auth_header into auth type and token
    sections = auth_header.split()
    if sections[0].lower() != 'bearer':
        raise AuthError({
            'code': 'Invalid Header',
            'description': 'Authorization header must be "Bearer"'
        }, 401)
    elif len(sections) == 1:
        raise AuthError({
            'code': 'Invalid Header',
            'description': 'Token Missing'
        }, 401)
    elif len(sections) > 2:
        raise AuthError({
            'code': 'Invalid Header',
            'description': 'Authorization header not bearer token'
        }, 401)
    # gets token from split auth_header
    token = sections[1]
    return token

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found'
        }, 401)
    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try: 
        unverified_header = jwt.get_unverified_header(token)
    except Exception as e:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token headers invalid'
        }, 401)
        abort(500)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except Exception as e:
                raise e
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator