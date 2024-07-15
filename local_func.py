import os
from os import path

from global_config import user_conf_path, user_cache_path, ALLOWED_EXTENSION


# INFO: Safety check for file
def check_file(filename):
    base_path = "/public/res/"
    full_path = path.normpath(path.join(base_path,
                                        filename)).replace("\\", "/")
    if ("." not in filename
            or filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSION):
        return "Illegal"
    if not full_path.startswith(base_path):
        return "Illegal"
    else:
        return filename


# XSS protection
def htmlspecialchars(text):
    return (text.replace("&", "&amp;").replace('"', "&quot;").replace(
        "<", "&lt;").replace(">", "&gt;"))


# Make sure all folders exist:
# |-- canvas/
# |   |-- .secret         // Automatically generated
# |   |-- user_configs/
# |   |-- user_caches/
def init_conf_path():
    if not os.path.exists("canvas"):
        os.mkdir("canvas")
        print("No canvas folder found. Created one.")
    if not os.path.exists(user_conf_path):
        os.mkdir(user_conf_path)
        print("No user configs folder found. Created one.")
    if not os.path.exists(user_cache_path):
        os.mkdir(user_cache_path)
        print("No user cache folder found. Created one.")


# Format url into https://example.com/
def url_format(url):
    if url.find("http://") == -1 and url.find("https://") == -1:
        # Invalid protocal
        url = "https://" + url
    if not url.endswith("/"):
        url = url + "/"
    return url
