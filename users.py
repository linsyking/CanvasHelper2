import base64
# import hashlib
import json
from os import path
from global_config import user_conf_path, user_cache_path, pwd_context


def conf_file_name(username):
    # return user_conf_path + hashlib.md5(
    #     username.encode()).hexdigest() + '.json'
    return user_conf_path + base64.b64encode(
        username.encode("ascii")).decode("utf-8") + '.json'


def cache_file_name(username):
    return user_cache_path + 'cache_' + base64.b64encode(
        username.encode("ascii")).decode("utf-8") + '.json'


def create_user(username, password):
    if user_exists(username):
        return False
    else:
        # create new file
        initial_conf = {
            "version": 1,
            "username": username,
            "hashed_password": pwd_context.hash(password),
            "semester_begin": "",
            "url": "",
            "bid": "",
        }
        # dump initial_conf to file as json
        with open(conf_file_name(username), 'w') as f:
            json.dump(initial_conf, f, ensure_ascii=False, indent=4)


def get_hashed_password(username):
    user_config_file = conf_file_name(username)
    if path.exists(user_config_file):
        with open(user_config_file, 'r') as f:
            user_info = json.load(f)
        return user_info.get('hashed_password')
    else:
        return None


def user_exists(username):
    if path.exists(conf_file_name(username)):
        return True
    else:
        return False
