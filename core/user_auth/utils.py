import datetime
from functools import wraps

import jwt
from flask import request

from .. import utils
from .. import Configuration

from . import models


def require_token(f):
    ''' 
    Decorator to restrict access allowing only valid authentication tokens and other constraints.
    token and other constraints should be provided in the request headers. 
    '''
    @wraps(f)
    def func(*args, **kwargs):
        
        REQUIRED_HEADERS = ['Authorization']
        OPTIONAL_HEADERS = ['']
        
        # Validate the request has the required headers
        for header in REQUIRED_HEADERS:
            if (header not in request.headers.keys()):
                raise KeyError('session authentication failed: missing required headers')
            
        # Validate authentication token.
        token = request.headers.get('Authorization')
        user = models.User.validate_token(token)
        
        if (not user):
            raise ValueError('session authentication failed: token is not valid')
        
    # Implement us
    # age limits on authenticated session (I.e. limit session/account to 100 requests per minute.)
        return f(*args, user=user, token=token, **kwargs)

    return func


# Use require_token to shorten this decorator
def require_admin(f):
    ''' Decorator to restrict access to admins only. '''
    @wraps (f)
    def func(*args, **kwargs):
        print('require_admin()')
        if ('Authorization' not in request.headers):
            return KeyError('Authentication token missing')

        token = request.headers.get('Authorization')
        print(f'token: {token}')
        user = models.User.validate_token(token)
        print (f'User: {user}')
        if (not user.is_admin):
            return ValueError("User is not an admin")

        kwargs['admin'] = user
        kwargs['token'] = token
        return f(*args, **kwargs)

    return func









