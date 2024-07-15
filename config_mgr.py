import sqlite3
import json
from global_config import DATABASE


class ConfigMGR:

    def __init__(self):
        pass  # No action is needed in constructor for now

    def get_conf(self, username):
        # example = {
        #     'username': 'test',
        #     'semester_begin': '2024-06-01',
        #     'url': 'https://canvas.com',
        #     'bid': '',
        #     'timeformat': 'relative',
        #     'background_image': 'aaa.jpg',
        #     'courses': [{
        #         'course_id': 847,
        #         'course_name': 'Physics',
        #         'type': 0,
        #         'maxshow': -1,
        #         'order': 'reverse',
        #         'msg': 'test1'
        #     }],
        #     'checks': []
        # }

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT * FROM users WHERE username = ?
                ''', (username, ))
            user_row = cursor.fetchone()
            if user_row:
                # Convert the row to a dictionary
                columns = [desc[0] for desc in cursor.description]
                user_db = [dict(zip(columns, user_row))][0]
                user_id = user_db['id']

                courses = self.get_courses(user_id, cursor)
                courses_list = [
                    dict(
                        zip([
                            'course_id', 'course_name', 'type', 'maxshow',
                            'order', 'msg'
                        ], course)) for course in courses
                ]

                checks = self.get_checks(user_id, cursor)
                checks_list = [
                    dict(zip(['type', 'item_id'], check)) for check in checks
                ]

                user_conf = {
                    "username": user_db['username'],
                    "semester_begin": user_db['semester_begin'],
                    "url": user_db['url'],
                    "bid": user_db['bid'],
                    "timeformat": user_db['timeformat'],
                    "background_image": user_db['background_image'],
                    "courses": courses_list,
                    "checks": checks_list
                }
                return user_conf
            else:
                return {"version": 1}

    def remove_key(self, username, key):
        self.set_key_value(username, key, None)

    def set_key_value(self, username, key, value):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # Get the user_id for the given username
            cursor.execute("SELECT id FROM users WHERE username = ?",
                           (username, ))
            user_id = cursor.fetchone()[0]

            if key == "courses":
                for course in value:
                    cursor.execute(
                        """
                            INSERT OR REPLACE INTO courses (
                                user_id, course_id, course_name, type, maxshow, display_order, msg
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (user_id, course['course_id'], course['course_name'],
                         course['type'], course['maxshow'], course['order'],
                         course['msg']))

            elif key == "checks":
                for check in value:
                    cursor.execute(
                        """
                            INSERT OR REPLACE INTO checks (
                                user_id, type, item_id
                            ) VALUES (?, ?, ?)
                        """, (user_id, check['type'], check['item_id']))

            elif key in [
                    "title", "semester_begin", "url", "bid", "timeformat",
                    "background_image"
            ]:
                for user_conf in value:
                    cursor.execute(
                        f"UPDATE users SET {key} = ? WHERE username = ?",
                        (user_conf, username))

            else:
                raise Exception("Invalid key")

            conn.commit()

    def get_checks(self, user_id, cursor):
        cursor.execute(
            '''
            SELECT type, item_id, type FROM checks WHERE user_id = ?
            ''', (user_id, ))
        return cursor.fetchall()

    def get_courses(self, user_id, cursor):
        cursor.execute(
            '''
            SELECT course_id, course_name, type, maxshow, display_order, msg FROM courses WHERE user_id = ?
            ''', (user_id, ))
        return cursor.fetchall()
