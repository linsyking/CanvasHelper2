import base64
# import hashlib
import json
from os import path
from global_config import *


def conf_file_name(username):
    # return user_conf_path + hashlib.md5(
    #     username.encode()).hexdigest() + '.json'
    return user_conf_path + base64.b64encode(
        username.encode("ascii")).decode("utf-8") + '.json'


def cache_file_name(username):
    return user_cache_path + 'cache_' + base64.b64encode(
        username.encode("ascii")).decode("utf-8") + '.json'


# def init_user(username):
#     if path.exists(conf_file_name(username)):
#         return True
#     else:
#         # create new file
#         with open(conf_file_name(username), 'w') as f:
#             f.write("{ \"version\": 1 }")
#             return False


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
