import datetime
from functools import wraps


from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


# Make imports from this module directory
from . import user_auth
from . import models

# Make imports from the top-level project directory.
from .. import utils
from .. import db
from .. import Configuration

# helper functions

def authenticated_session(f):
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
                return utils.response('session authentication failed: missing required headers')
            
        # Validate authentication token.
        token = request.headers.get('Authorization')
        user = validate_authentication_token(token)
        
        if (not user):
            return utils.response('session authentication failed: token is not valid')
        
        # Implement usage limits on authenticated session (I.e. limit session/account to 100 requests per minute.)
        return f(*args, user=user, **kwargs)

    return func



def generate_authentication_token(public_id, expires_time=None):
    ''' 
    Generate an authentication token.
    Do this by encoding the user's (private key or public key??),
    the time the token is created and the expiration time.
    '''
    token_data = {
        'id': public_id,
        'created': datetime.datetime.now().isoformat(),
        'expires': expires_time.isoformat() if expires_time else 
                   (datetime.datetime.now() + datetime.timedelta(hours=6)).isoformat(),
        
    }
    token = jwt.encode(token_data, Configuration.SECRET_KEY, "HS256")
    return token


def validate_authentication_token(token):
    """
    The first iteration should simply check that the authentication token belongs to a user and the time is not expired.
    The second iteration should go about solving the storage of this token on the server side for better authentication.

    Args:
        token (string): a token provided by the server upon successful authentication or presistence validation.

    Returns:
        User or None: The result of the validation.
    """
    token_data = jwt.decode(token, Configuration.SECRET_KEY, "HS256")
    token_data['expires'] = datetime.datetime.fromisoformat(token_data['expires'])
    
    # Exit Conditions:
    # 1. The token has expired.
    expires_in = token_data['expires'].timestamp() - datetime.datetime.now().timestamp()
    if (expires_in < 0):
        return None 
    
    # 2. The token's signer does not exist.
    user = models.User.query.filter_by(id=token_data['id']).first()
    if (user == None):
        return None
    
    # 3. The token has not persisted on the server (extra).
    if (user.token != token):
        return None
    
    return user
    

# view functions

@user_auth.route('/user_auth/test')
def index ():
    ''' Test that this module is accessible. '''
    return utils.response('testing successful') 


@user_auth.route('/register', methods=['POST'])
def register():
    """ Given an unused email and a password register the user. """
    
    data = request.get_json()
    
    # Verify that the recieved json has the required fields
    FIELDS = ['email', 'password']
    for field_name in FIELDS:
        if field_name not in data.keys():
            return utils.response('request must include an email and password')
    
    
    # Check if the user is already registered.
    results = models.User.query.filter_by(email=data['email']).first()
    if (results != None): 
        return utils.response('email is already registered')
    
    try:
        # create the new user after generating a password-hash, a unique user_id, and an authentication token.
        user_id = models.generate_unique_user_id()
        token = generate_authentication_token(user_id)
        password_hash = generate_password_hash(data['password'], method='sha256')
        kwargs = {'id': user_id, 'password': password_hash, 'email': data['email'], 'token': token}

        new_user = models.User(**kwargs)
    except Exception as e:
        return utils.response('could not create user', body=str(e))


    try:
        # Save the newly created user to the database.
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return utils.response('registration failed', body=str(e))
    
    
    # email verification (v2).
    ## if available provide email verification.

    response = {}
    response['Authorization'] = token
    return utils.response('registration successful', body=response)
    


@user_auth.route('/login', methods=['POST'])
def login():
    """ 
    Attempt a user login using the provided email and password. 
    Return an authentication token upon successful login. 
    """
    data = request.get_json()
    FIELDS = ['email', 'password']
    for field in FIELDS:
        if field not in data.keys():
            return utils.response('request must include an email and password')
        
    # Verify a user has the given email 
    user = models.User.query.filter_by(email=data['email']).first()
    if (user == None):
        return utils.response('invalid email address')
    
    # verify that the given password is correct by checking the stored hash.
    verified = check_password_hash(user.password, data['password'])
    if (not verified): 
        return utils.response('incorrect password')
    
    
    try:
        # Generate a new authentication token
        user.token = generate_authentication_token(user.id)
        db.session.commit()
    except Exception as e:
        return utils.response('could not save authentication token', body=str(e))    
    
    response = {
        'Authorization': user.token,
    }
    
    # return an authentication token upon successful login
    return utils.response('login success. authentication token provided.', body=response)



@user_auth.route('/logout', methods=['POST'])
@authenticated_session
def logout(user):
    '''
    Revoke's the session authentication token's validity.
    
    The user variable is provided by the @authenticated_session decorator.
    '''
    try:
        # nullify the authentication token in the database.
        user.token = None
        db.session.commit()
    except Exception as e:
        return utils.response('could not purge the session authentication token.')
    
    return utils.response('logout successful')



@user_auth.route('/users/all')
def get_all_users():
    # users = [{'email': user.email, 'password': user.password} for user in models.User.query.all()]
    users = [user.serialize for user in models.User.query.all()]
    return utils.response(users=users)