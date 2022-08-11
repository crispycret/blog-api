import uuid

from .. import db


def generate_unique_user_id():
    """ Verify that no User has the same user_id. """
    # Generate a random user id.
    user_id = str(uuid.uuid4())

    # Check to see if the user id has already been used.
    results = User.query.filter_by(id=user_id).first()

    # Try generating random uuid's until a unique one is found. 
    if (results != None):
        # loop the call until an unused user_id is generated.
        # user_id = create_random_user_id()
        return generate_unique_user_id()
    
    return user_id



class User(db.Model):
    
    pk = db.Column(db.Integer, primary_key=True)
    
    id = db.Column(
        db.String(256), default=generate_unique_user_id
    )

    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    
    token = db.Column(db.String(255), nullable=True)
    
    
    @property
    def serialize(self):
        return {'pk': self.pk, 'id':self.id,'email': self.email, 'password': self.password, 'token': self.token}
    
    
    
