from datetime import datetime, timedelta
from jose import jwt, JWTError
import random
import os

from global_config import ALGORITHM, pwd_context
from users import user_exists, get_hashed_password


# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    if not user_exists(username):
        return False
    elif not verify_password(password, get_hashed_password(username)):
        return False
    else:
        return username


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(*, data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def gen_key():  # Prevent key leak like Nacos CNVD-2023674205
    secret_file = './canvas/.secret'
    if not os.path.exists(secret_file):
        SECRET_KEY = ''.join(
            random.choice('0123456789abcdef') for _ in range(32))
        with open(secret_file, 'w') as f:
            f.write(SECRET_KEY)
        print('No ' + secret_file + ' found. Generated new secret key')
        return SECRET_KEY
    else:
        print('Found ' + secret_file + '. Using existing secret key')
        with open(secret_file, 'r') as f:
            return f.read()


def verify_login(auth_token):
    # Same as verify_cookie, but take string as input
    if not auth_token:  # No auth_token in cookie
        return False
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access_token":
            return False
        username: str = payload.get("sub")
        if not username:
            return False
    except JWTError:
        return False
    # Not None indicates a valid token
    if not user_exists(username):
        return False
    return username


SECRET_KEY = gen_key()  # if no key stored, generate a new one

if __name__ == "__main__":
    while True:
        password = input("Password: ")
        print(get_password_hash(password))
