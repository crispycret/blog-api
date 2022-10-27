from enum import unique
import uuid

import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from .. import Configuration

from . import utils

now = datetime.datetime.now

def generate_public_id():
    """ Verify that no User has the same user_id. """
    # Generate a random user id.
    user_id = str(uuid.uuid4())

    # Check to see if the user id has already been used.
    results = User.query.filter_by(id=user_id).first()

    # Try generating random uuid's until a unique one is found. 
    if (results):
        # loop the call until an unused user_id is generated.
        # user_id = create_random_user_id()
        return User.generate_unique_public_id()
    
    return user_id



class Token(db.Model):
    ''' Authentication Token for user sessions. '''
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token = db.Column(db.String(256), unique=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
        }

    @staticmethod
    def exists(token):
        ''' Return True or False for if the token is stored in the database'''
        return Token.query.filter_by(token=token).first()

    @staticmethod
    def decode_token(token):
        ''' Decode the token string and return a token object '''
        data = jwt.decode(token, Configuration.SECRET_KEY, 'HS256')
        data['created'] = datetime.datetime.fromisoformat(data['created'])
        data['expires'] = datetime.datetime.fromisoformat(data['expires'])
        return data

    @staticmethod
    def is_valid(token):
        ''' Return True or False for if the encoded token is valid. '''
        data = Token.decode_token(token)
        time_left = data['expires'].timestamp() - now().timestamp()
        if (time_left <= 0):
            return False
        return True



# Redesign user to use a basic autoincrement id.
# generate a public id for public use
# generate a private id for private use
# remove token and create a sepeate table if needed for tokens.
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(256), default=generate_public_id)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    tokens = db.relationship('Token', backref='user', lazy=True, cascade='all, delete-orphan')
    
    
    @property
    def serialize(self):
        return {
            'id': self.id, 
            'public_id':self.public_id,
            'email': self.email, 
            'password': self.password,
            'is_admin': self.is_admin,
        }
    

    def verify_password(self, password):
        ''' Return the results of checking the password to the stored hash. '''
        return check_password_hash(self.password, password)

    def generate_token(self, expires=None):
        ''' Generate an authentication token for the user. '''
        created = now()
        if (not expires):
            expires = created + datetime.timedelta(month=1)

        token = {
            'public_id': self.public_id,
            'created': created.isoformat(),
            'expires': expires.isoformat(),
        }
        token = jwt.encode(token, Configuration.SECRET_KEY, 'HS256')
        token = Token(user_id=self.id, token=token)
        return token
    
    def remove_invalid_tokens(self):
        ''' Purge any invalid tokens stored in the database for the user '''
        tokens = Token.query.filter_by(user_id=self.id).all()
        for token in tokens:
            if (not Token.is_valid(token.token)):
                db.session.delete(token)
        
        db.session.commit()
        return True


    @staticmethod
    def create(email, password):
        ''' Create a new user with a unique public id and has the password. '''
        public_id = generate_public_id()
        password_hash = generate_password_hash(password, method='sha256')
        data = {
            'public_id': public_id, 
            'password': password_hash, 
            'email': email,
            'is_admin': False
        }

        return User(**data)

    @staticmethod
    def validate_token(token):
        ''' decode the token and return the corresponding user if the token is valid. '''
        # Rename to get_by_token() or from_token()
        print ('validate_token()')
        data = Token.decode_token(token)
        print (f'data: {data}')

        if (not Token.is_valid(token)):
            return None

        if (not Token.exists(token)):
            return None

        # return the user if the token is valid
        return User.query.filter_by(public_id=data['public_id']).first()


    @staticmethod
    def exists(email):
        return User.query.filter_by(email=email).first()
    


    @staticmethod
    def login(user):
        pass



