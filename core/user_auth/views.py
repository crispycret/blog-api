import datetime
from functools import wraps


from flask import request
import jwt


# Make imports from this module directory
from . import user_auth
from . import models

# Make imports from the top-level project directory.
from .. import utils
from .. import db
from .. import Configuration

from .utils import require_admin, require_token 



'''
create_admin() -> Application Secret Key
get_all_users() -> is_admin

register() -> email, password
login() -> email, password
logout() -> token
delete_user() -> token or is_admin

'''


@user_auth.route('/user_auth/test')
def index ():
    ''' Test that this module is accessible. '''
    return utils.response('testing successful') 


@user_auth.route('/admin/create', methods=['POST'])
def create_admin():
    ''' Create an admin user. Requires application secret key? '''
    if ('Authorization' not in request.headers):
        return {'status': 400, 'msg': 'missing authorization token', 'body': {}}
    
    # Verify application secret key
    token = request.headers['Authorization']
    data = jwt.decode(token, Configuration.ADMIN_SECRET_KEY, 'HS256')
    print (data)
    try:
        user = models.User.create(data['email'], data['password'])
        user.is_admin = True
        print(user.serialize)
        db.session.add(user)
        db.session.commit()
        return {'status': 200, 'msg': 'created admin', 'body': user.serialize}
    except Exception as e:
        return {'status': 400, 'msg': 'create admin failed', 'body': str(e)}




@user_auth.route('/register', methods=['POST'])
def register():
    """ Given an unused email and a password register the user. """
    
    data = request.get_json()
    
    try:
        user = models.User.create(data)
        db.session.add(user)
        db.session.commit()
        return {'status': 200, 'msg': 'user registered', 'body': user.serialize}
    except Exception as e: 
        return {'status': 400, 'msg': 'user not registered', 'body': str(e)}    
 
    # email verification (v2).
    ## if available provide email verification.



@user_auth.route('/login', methods=['POST'])
def login():
    """ 
    Attempt a user login using the provided email and password. 
    Return an authentication token upon successful login.
    Upon login remove old invalid tokens
    """
    data = request.get_json()

    try:
        # Verify user exists
    
        user = models.User.exists(data['email'])
        if (not user):
            return {'status': 400, 'msg': 'login failed: no user exits with provided email', 'body': {}}
        
        if (not user.verify_password(data['password'])):
            return {'status': 400, 'msg': 'login failed: password incorrect', 'body': {}}

        try:
            user.remove_invalid_tokens()    
        except Exception as e:
            return {'status': 400, 'msg': 'could not remove expired tokens', 'body': str(e)}

        expires = datetime.datetime.now() + datetime.timedelta(days=1)
        token = user.generate_token(expires=expires)

        db.session.add(token)
        db.session.commit()

        response = {'Authorization': token.token}
        return {'status': 200, 'msg': 'login success', 'body': response}
    except Exception as e:
        return {'status': 400, 'msg': 'login failed', 'body': str(e)}



@user_auth.route('/logout', methods=['POST'])
@require_token
def logout(user, token):
    '''
    Revoke's the session authentication token's validity.
    The user variable is provided by the @authenticated_session decorator.
    ''' 
    try:
        # nullify the authentication token in the database.
        if (not models.Token.exists(token)):
            return {'status': 400, 'msg': 'token does not exist', 'body': {}}

        db.session.delete(token)
        db.session.commit()
        return {'status': 200, 'msg': 'token removed', 'body': {}}
    except Exception as e:
        return {'status': 400, 'msg': 'failed to remove token', 'body': str(e)}
    


@user_auth.route('/user/delete', methods=['DELETE'])
@require_token
def delete_user(user, token):
    ''' Remove a user if the requester is that user or is the admin. '''
    # In case it is the admin removing a user, expect the user to remove in json
    if (user.is_admin):
        data = request.get_json()

        # Replace `user` with the user to delete.
        try:
            user = models.User.query.filter_by(id=data['user_id'])
        except Exception as e:
            return {'status': 400, 'msg': 'user not found', 'body': str(e)}

    try:
        db.session.delete(user)
        db.session.commit()
        return {'status': 200, 'msg': 'user deleted', 'body': {}}
    except Exception as e:
        return {'status': 400, 'msg': 'failed to delete user', 'body': str(e)}


@user_auth.route('/users/all')
@require_admin
def get_all_users(admin, token):
    # users = [{'email': user.email, 'password': user.password} for user in models.User.query.all()]
    try:
        users = [user.serialize for user in models.User.query.all()]
        return {'status': 200, 'msg': 'retrieved all users', 'body': {'users': users}}
    except Exception as e:
        return {'status': 400, 'msg': 'failed to remove token', 'body': str(e)}
    





