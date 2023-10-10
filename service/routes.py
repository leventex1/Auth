from flask import Blueprint, request
from service import db
from service.model import User, RefreshToken

from service.utils.passwordhash import generate_password_hash, valid_password_hash
from service.utils.token import generate_unique_token, generate_access_token, is_valid_access_token
from datetime import datetime

routes = Blueprint('routes', __name__)


"""
    Register a user in the database.
"""
@routes.post('/auth/user')
def register_user():
    
    data = request.json

    email = data.get('email')
    password = data.get('password')

    if not isinstance(email, str) or not isinstance(password, str):
        return { 'message': 'Invalid data.' }, 400

    try:
        user: User = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        refresh_token = RefreshToken(user_id=user.id)
        db.session.add(refresh_token)
        db.session.commit()
    except:
        return { 'message': 'User already exists.' }, 409

    return { 'message': 'User created.' }, 200


"""
    Logs in a user, issue an access/refresh token pair.
"""
@routes.put('/auth/user')
def login_user():

    data = request.json

    email = data.get('email')
    password = data.get('password')

    if not isinstance(email, str) or not isinstance(password, str):
        return { 'message': 'Invalid data.' }, 400
    
    try:
        user: User = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
        if not valid_password_hash(hashed_password=user.password, password=password):
            raise ValueError()
    except:
        return { 'message': 'User not found.' }, 404

    user.refresh_token.token = generate_unique_token()
    db.session.commit()

    access_token = generate_access_token(user_id=user.id)

    return { 
        'message': 'User logged in.', 
        'refresh_token': user.refresh_token.token,
        'access_token': access_token
    }, 200


"""
    Check if the access token is valid. Returns the user_id if valid.
"""
@routes.get('/auth/user/access_token/<access_token>')
def chcek_access_token(access_token: str):

    decoded_message = is_valid_access_token(access_token)

    if not decoded_message:
        return { 'message': 'Access token is not valid.' }, 401
    
    return { 'message': 'Access token is valid.', 'user_id': decoded_message.get('user_id') }, 200


"""
    Issue a new refresh/access token pair if the refresh token is valid.
"""
@routes.get('/auth/user/refresh_token/<refresh_token>')
def check_refresh_token(refresh_token: str):

    try:
        refresh_token_db: RefreshToken = db.session.execute(db.select(RefreshToken).filter_by(token=refresh_token)).scalar_one()
        if datetime.utcnow() >= refresh_token_db.valid_until:
            raise ValueError()
    except:
        return { 'message': 'Refresh token is not valid.' }, 401
    
    refresh_token_db.token = generate_unique_token()
    db.session.commit()

    access_token = generate_access_token(user_id=refresh_token_db.user.id)

    return {
        'message': 'New access/Refresh token pair issued.',
        'refresh_token': refresh_token_db.token,
        'access_token': access_token
    }, 200
    
