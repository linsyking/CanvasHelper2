#!/usr/bin/env python3
'''
@Author: King
@Date: 2023-01-04 09:17:45
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

import json
from os import path

'''
Configuration Manager

Configuration is located in ./user_conf.json
It will include:
- Canvas configuration
- Wallpaper configuration
- All courses configuration
'''


class ConfigMGR:
    configuration = None

    def __init__(self):
        if not path.exists('user_conf.json'):
            # Create this configuration file
            self.configuration = {
                "version": 1,
            }
            self.write_conf()
        else:
            self.force_read()
            if self.configuration['version'] != 1:
                raise Exception('Error: Configuration file version mismatch!')

    def write_conf(self):
        '''
        Write configuration to the local file.
        '''
        self.check_health()
        with open('./user_conf.json', 'w', encoding='utf-8', errors='ignore') as f:
            json.dump(self.configuration, f, ensure_ascii=False, indent=4)

    def get_conf(self):
        return self.configuration

    def remove_key(self, key: str):
        self.configuration.pop(key)
        self.write_conf()

    def force_read(self):
        '''
        Read configuration file.
        '''
        with open('./user_conf.json', 'r', encoding='utf-8', errors='ignore') as f:
            self.configuration = json.load(f)

    def check_health(self):
        if not self.configuration:
            raise Exception('No configuration found')

    def set_key_value(self, key, value):
        self.configuration[key] = value
        self.write_conf()

    def update_conf(self, conf):
        '''
        Update the whole configuration
        '''
        self.configuration = conf
        self.write_conf()

    def set_wallpaper_path(self, path):
        self.configuration['wallpaper_path'] = path
