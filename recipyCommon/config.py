"""
Configuration file-related functions for recipy
"""

try:
    from ConfigParser import SafeConfigParser, Error
except:
    from configparser import SafeConfigParser, Error

import os
import sys

from distutils.spawn import find_executable


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


def get_editor():
    try:
        editor = conf.get('general', 'editor')
    except Error:
        if os.environ.get('EDITOR'):
            editor = '$EDITOR'
        else:
            editor = find_editor()
    if editor is None or editor is '':
        raise RuntimeError("Cannot launch text editor. "
                           "Try setting the editor in the ~/.recipy/recipyrc file")

    return editor


def find_editor():
    """ Attemps to find a valid text editor by trying different executables (according to the operating system) and
    checking for existence. """
    platform = sys.platform

    # open the empty file by trying different text editors according to the operating system
    if "linux" in platform:
        editor = _try_editors(["/usr/bin/editor", "nano", "vi", "emacs"])
    elif "darwin" in platform:  # macintosh
        editor = _try_editors(["nano", "vi", "emacs", "open -t"])
    elif "win" in platform:  # windows
        editor = _try_editors(["edit", "notepad", "notepad.exe"])
    else:
        editor = None
    return editor


def _try_editors(list_of_commands):
    for command in list_of_commands:
        exe = command.split(' ')[0]  # strip the options
        exe_path = find_executable(exe)
        if exe_path is not None:
            return command
    return None  # returns None if no editor is found


def get_gui_port():
    try:
        return int(conf.get('general', 'port'))
    except Error:
        return 9000
