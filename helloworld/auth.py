# -*- coding: utf-8 -*-
import functools
import flask
import jwt
import base64
from datetime import datetime
from werkzeug.exceptions import Unauthorized, Forbidden
import helloworld


def requires_auth(f):
    """
    Requires user authentication information to be supplied as a JWT.

    Decorator function for Flask requests. If the JWT can be decoded successfully, ``flask.g.user`` will be set with the
    JWT payload.

    :param f: function or method to be decorated
    :return: decorated function
    """

    @functools.wraps(f)
    def decorated_f(*args, **kwargs):
        token = auth_token(flask.request.headers)
        flask.g.user = authenticate_user(token)
        return f(*args, **kwargs)

    return decorated_f


def requires_role(role):
    """
    Requires user authentication information to be supplied as a JWT with ``role`` in ``payload['roles']``.

    Decorator function for Flask requests. If the JWT can be decoded successfully, ``flask.g.user`` will be set with the
    JWT payload.

    :param role: required role
    :type role: str
    :return: decorated function
    """

    def decorate(f):
        def decorated_f(*args, **kwargs):
            token = auth_token(flask.request.headers)
            user = authenticate_user(token)
            try:
                if role not in user["roles"]:
                    raise Forbidden('Requires role `{}`'.format(role))
            except KeyError:
                raise Forbidden('No roles provided in token')

            flask.g.user = user
            return f(*args, **kwargs)

        return decorated_f

    return decorate


def auth_token(headers):
    """
    Return Bearer token from Authorization header.

    Raises :class:`werkzeug.exceptions.Unauthorized` if no or invalid Authorization header provided.

    :param headers: request headers
    :type headers: dict
    :return: Bearer token
    :rtype: str
    """
    auth = headers.get('Authorization', None)
    if not auth:
        raise Unauthorized('Authorization header is expected')
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise Unauthorized('Authorization header must start with Bearer')
    elif len(parts) == 1:
        raise Unauthorized('Token not found')
    elif len(parts) > 2:
        raise Unauthorized('Authorization header must be Bearer + \s + token')

    return parts[1]


def authenticate_user(token):
    """
    Authenticate and return user from JSON Web Token.

    Raises :class:`werkzeug.exceptions.Unauthorized` if token is invalid.

    :param token: JWT
    :type token: str
    :return: user
    :rtype: dict
    """
    client_id = helloworld.app.config['AUTH_CLIENT_ID']
    client_secret = helloworld.app.config['AUTH_CLIENT_SECRET']
    try:
        return jwt.decode(
            token,
            base64.b64decode(client_secret.replace("_", "/").replace("-", "+")),
            audience=client_id
        )
    except jwt.ExpiredSignature:
        raise Unauthorized('Token is expired')
    except jwt.InvalidAudienceError:
        raise Unauthorized('Incorrect audience')
    except jwt.DecodeError:
        raise Unauthorized('Token signature is invalid')
    except jwt.InvalidTokenError:  # jwt base exception
        raise Unauthorized('Token invalid')


def create_jwt(payload, set_audience=True):
    """
    Return a JSON Web Token with data ``payload``.

    Automatically adds ``aud`` to payload if ``set_audience``.

    :param payload: data to encode in jwt
    :type payload: dict
    :param set_audience: whether to set the audience info
    :type set_audience: bool
    :return: JWT
    :rtype: str
    """
    secret = helloworld.app.config['AUTH_CLIENT_SECRET']
    signature = base64.b64decode(secret.replace("_", "/").replace("-", "+"))
    if set_audience:
        payload['aud'] = helloworld.app.config['AUTH_CLIENT_ID']
    payload['iat'] = datetime.utcnow()
    return jwt.encode(payload, signature).decode('utf-8')  # return as string instead of bytes