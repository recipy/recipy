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
    
    # Try reading files in the current directory first
    files_read = CONFIG.read(['.recipyrc', 'recipyrc'])

    # Read the config file in the home directory
    if len(files_read) == 0:
        CONFIG.read(os.path.expanduser("~/.recipy/recipyrc"))

    return CONFIG


conf = read_config_file()

def option_set(section, name):
    return conf.has_option(section, name)

def get_db_path():
    try:
        return conf.get('database', 'path')
    except Error:
        return os.path.expanduser('~/.recipy/recipyDB.json')
    
def get_gui_port():
    try:
        return int(conf.get('general', 'port'))
    except Error:
        return 9000
