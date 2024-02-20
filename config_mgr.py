#!/usr/bin/env python3

from os import path
import json

from users import conf_file_name

class ConfigMGR:
    def __init__(self):
        pass  # No action needed in constructor for per-user config

    def get_conf(self, username):
        config_file = conf_file_name(username)
        if path.exists(config_file):
            with open(config_file, "r", encoding="utf-8", errors="ignore") as f:
                return json.load(f)
        else:
            # Return a default configuration or raise an error
            return {
                "version": 1,
                # Add more default settings if necessary
            }

    def write_conf(self, username, configuration):
        config_file = conf_file_name(username)
        with open(config_file, "w", encoding="utf-8", errors="ignore") as f:
            json.dump(configuration, f, ensure_ascii=False, indent=4)

    def remove_key(self, username, key):
        configuration = self.get_conf(username)
        configuration.pop(key, None)  # Use pop with default to avoid KeyError
        self.write_conf(username, configuration)

    def set_key_value(self, username, key, value):
        configuration = self.get_conf(username)
        configuration[key] = value
        self.write_conf(username, configuration)

    def update_conf(self, username, conf):
        self.write_conf(username, conf)

    def set_wallpaper_path(self, username, path):
        self.set_key_value(username, "wallpaper_path", path)
