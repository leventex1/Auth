from service import app
from datetime import datetime, timedelta

def get_expiration_access_token():
    with app.app_context():
        exp = datetime.utcnow() + timedelta(minutes=app.config.get('ACCESS_EXP_MINUTES'))
    return exp

def get_expiration_refresh_token():
    with app.app_context():
        exp = datetime.utcnow() + timedelta(days=app.config.get('REFRESH_EXP_DAYS'))
    return exp