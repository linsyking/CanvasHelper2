import sqlite3

from global_config import DATABASE


def get_cache(username):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username, ))
        user_id = cursor.fetchone()[0]
        cursor.execute(
            '''
            SELECT html FROM user_cache WHERE user_id = ?
            ''', (user_id, ))
        return cursor.fetchone()
