from service import bcrypt

def generate_password_hash(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')

def valid_password_hash(hashed_password: str, password: str) -> bool:
    return bcrypt.check_password_hash(hashed_password, password)