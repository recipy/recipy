"""
Helper functions for recipy tests.
"""

# Copyright (c) 2016 University of Edinburgh.

import os
import os.path
import shutil

try:
    from ConfigParser import SafeConfigParser
except:
    from configparser import SafeConfigParser

from integration_test import database
from integration_test import recipy_environment as recipyenv


def update_recipyrc(recipyrc, section, key, value=None):
    """
    Update recipyrc configuration file.

    :param recipyrc: recipyrc configuration file
    :type recipyrc: str or unicode
    :param section: configuration section, created if it does not
    exist
    :type section: str or unicode
    :param key: key
    :type key: str or unicode
    :param value: value, optional for key-only parameters
    :type value: str or unicode
    """
    config = SafeConfigParser(allow_no_value=True)
    config.read(recipyrc)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)
    with open(recipyrc, "w") as configfile:
        config.write(configfile)


def get_log(recipydb):
    """
    Get the latest log from the database along with its
    'filediffs', if any.

    :param recipydb: recipydb path
    :type recipydb: str or unicode
    :return: log
    :rtype: dict
    :return: log and filediffs. If no 'filediffs' then this value
    is None. If no log exists then None is returned.
    :rtype: (dict, dict)
    """
    connection_data = {database.TINYDB_PATH: recipydb}
    connection = database.open_db(connection_data)
    latest = database.get_latest_id(connection)
    (log_number, log) = database.get_log(connection, latest)
    diffs = database.get_filediffs(connection, log_number)
    database.close_db(connection)
    return (log, diffs)


def clean_recipy():
    """
    Empty ~/.recipy, deletes recipyrc and .recipyrc.
    """
    recipy_dir = recipyenv.get_recipy_dir()
    if os.path.isdir(recipy_dir):
        shutil.rmtree(recipy_dir)
    os.mkdir(recipy_dir)
    for path in [recipyenv.get_local_recipyrc(),
                 recipyenv.get_local_dotrecipyrc()]:
        if os.path.isfile(path):
            os.remove(path)


def enable_recipy(source, destination):
    """
    Copy a Python script and insert 'import recipy' as its first
    line.

    :param source: Python script to be copied
    :type source: str or unicode
    :param destination: Copy of Python script
    :type destination: str or unicode
    """
    with open(source, "r") as source_file:
        lines = source_file.readlines()
    with open(destination, "w") as destination_file:
        destination_file.write("import recipy\n")
        destination_file.writelines(lines)
