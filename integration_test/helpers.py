"""
Helper functions for recipy tests.
"""

# Copyright (c) 2016 University of Edinburgh.

import os
import os.path
import re
import shutil

try:
    from ConfigParser import SafeConfigParser
except:
    from configparser import SafeConfigParser

from integration_test import database
from integration_test import environment
from integration_test import process
from integration_test import recipy_environment as recipyenv


def get_environment_value(env_var, default_value):
    """
    Get an environment value.

    * If an environment variable with name 'env_var' is defined,
      then its value is returned.
    * Else, 'default_value' is returned.

    :param env_var: Environment variable with value
    :type env_var: str or unicode
    :param default_value: Default value
    :type default_value: str or unicode
    :return: value
    :rtype: str or unicode
    """
    if env_var in os.environ:
        value = os.environ[env_var]
    else:
        value = default_value
    return value


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


def get_number_of_logs(recipydb):
    """
    Get the number of logs in the database.

    :param recipydb: recipydb path
    :type recipydb: str or unicode
    :return: Number of logs
    :rtype: int
    """
    connection_data = {database.TINYDB_PATH: recipydb}
    connection = database.open_db(connection_data)
    number_of_logs = database.number_of_logs(connection)
    database.close_db(connection)
    return number_of_logs


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


def assert_matches_regexps(string, regexps):
    """
    Look for each regular expression pattern in a string.

    :param string: String
    :type string: str or unicode
    :param destination: Regular expressions
    :type destination: list of str or unicode
    :raises AssertionError: if any regular expression cannot be found
    """
    for regexp in regexps:
        match = re.search(regexp, string)
        assert match is not None, ("Expected " + regexp)


def assert_equal_json_logs(log1, log2):
    """
    Compare two recipy JSON logs for equality.

    :param log1: Log
    :type log1: dict
    :param log2: Another log
    :type log2: dict
    :raises AssertionError: if log1 and log2 differ in their keys
    and/or values
    """
    # Convert dates from str or unicode to datetime.datetime.
    for key in ["date", "exit_date"]:
        log1[key] = environment.get_tinydatestr_as_date(log1[key])
        log2[key] = environment.get_tinydatestr_as_date(log2[key])
    assert log1 == log2, "Expected equal logs"


def execute_python(arguments, exit_status=0):
    """
    Run script using current Python executable.

    :param arguments: Arguments to Python
    :type arguments: list of str or unicode
    :param exit_status: Expected exit status
    :type exit_status: int
    :return: (exit code, standard output and error)
    :rtype: (int, str or unicode)
    :raises AssertionError: if actual exit status does not match
    exit_status
    """
    actual_exit_status, stdout = process.execute_and_capture(
        environment.get_python_exe(), arguments)
    assert exit_status == actual_exit_status,\
        ("Unexpected exit code " + str(actual_exit_status))
    return actual_exit_status, stdout
