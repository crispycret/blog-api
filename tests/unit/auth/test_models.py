from core.user_auth import models
from werkzeug.security import check_password_hash, generate_password_hash


def test_create_admin(): 
    """ 
    Given an User model
    WHEN a new User is created and is_admin is set True
    THEN check the email, password, and is_admin field is set correctly.
    """
    email = 'someuser@email.com'
    password = 'myPassword'
    user = models.User.create(email, password)
    user.is_admin = True

    assert user.public_id != None
    assert user.email == email
    assert check_password_hash(user.password, password) == True
    assert user.is_admin == True


def test_create_user(): 
    """ 
    Given an User model
    WHEN a new User is created and is_admin is set True
    THEN check the email, password, and is_admin field is set correctly.
    """
    
    email = 'someuser@email.com'
    password = 'myPassword'
    user = models.User.create(email, password)
    user.is_admin = True

    assert user.public_id != None
    assert user.email == email
    assert check_password_hash(user.password, password) == True
    assert user.is_admin == False



