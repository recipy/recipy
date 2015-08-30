"""
Configuration file-related functions for recipy
"""

try:
    from ConfigParser import SafeConfigParser, Error
except:
    from configparser import SafeConfigParser, Error

import os

def read_config_file():
    """
    Reads the recipy configuration file, which is in Windows INI-style format

    Try .recipyrc and recipy in the current directory, and then ~/.recipy/recipyrc
    """
    CONFIG = SafeConfigParser(allow_no_value=True)
    CONFIG.read(['.recipyrc', 'recipyrc', os.path.expanduser("~/.recipy/recipyrc")])

    return CONFIG


conf = read_config_file()

def option_set(section, name):
    return conf.has_option(section, name)

def get_db_path():
    try:
        return conf.get('database', 'path')
    except Error:
        return os.path.expanduser('~/.recipy/recipyDB.json')
    