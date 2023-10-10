from flask import current_app
from uuid import uuid4
import jwt
from datetime import datetime, timedelta

# Generates a general purops unique token.
def generate_unique_token() -> str:
    return str(uuid4())

def generate_access_token(user_id: str) -> str:
    encoded_jwt = jwt.encode(
        { 
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=current_app.config.get('ACCESS_EXP_MINUTES'))
        }, 
        current_app.config.get('SECRET_KEY'), 
        algorithm='HS256'
    )
    return encoded_jwt

# Returns the decoded token's message if valid else None.
def is_valid_access_token(token: str) -> dict:
    try: 
        decoded_jwt = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return decoded_jwt
    except:
        return None