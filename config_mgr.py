#!/usr/bin/env python3
'''
@Author: King
@Date: 2023-01-04 09:17:45
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

'''
Configuration manager

Configuration is located in __FILE__/user_conf.json
It will include:
- Canvas configuration
- Wallpaper configuration
- All courses configuration
'''

class ConfigMGR:
    configuration = None

    def check_health(self):
        if not self.configuration:
            raise Exception('No configuration found')
    

    def set_wallpaper_path(self, path):
        self.configuration['wallpaper_path'] = path
