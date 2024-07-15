import sqlite3
from global_config import DATABASE, pwd_context


def create_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        if user_exists(username, cursor):
            return False
        else:
            hashed_password = pwd_context.hash(password)
            cursor.execute(
                '''
                INSERT INTO users (username, hashed_password) VALUES (?, ?)
            ''', (username, hashed_password))
            conn.commit()
            return True


def get_hashed_password(username):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT hashed_password FROM users WHERE username = ?
        ''', (username, ))
        result = cursor.fetchone()
        return result[0] if result else None


def user_exists(username, cursor=None):
    if cursor is None:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            return user_exists(username, cursor)
    else:
        cursor.execute(
            '''
            SELECT id FROM users WHERE username = ?
        ''', (username, ))
        return cursor.fetchone() is not None
