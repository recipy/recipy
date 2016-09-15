"""
File utilities.
"""

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import json
import os
import yaml


def load_file(file_name):
    """Load the contents of a YAML or JSON file.

    :param file_name: File name with extension .yaml, .yml, json or
    .jsn
    :type file_name: str or unicode
    :return: content
    :rtype: dict
    :raises IOError: if the file is not found
    :raises FileContentError: if there is a problem parsing the file
    """
    _, ext = os.path.splitext(file_name)
    if ext.lower() in [".yaml", ".yml"]:
        return load_yaml(file_name)
    elif ext.lower() in [".json", ".jsn"]:
        return load_json(file_name)
    raise ValueError(file_name + " has an unrecognised extension")


def load_yaml(file_name):
    """Load the contents of a YAML file.

    :param file_name: File name
    :type file_name: str or unicode
    :return: content or None if file is empty
    :rtype: dict
    :raises IOError: if the file is not found
    :raises FileContentError: if there is a problem parsing YAML
    """
    with open(file_name, 'r') as f:
        try:
            content = yaml.load(f)
        except yaml.YAMLError as e:
            raise FileContentError(file_name, e)
    return content


def load_json(file_name):
    """Load the contents of a JSON file.

    :param file_name: File name
    :type file_name: str or unicode
    :return: content
    :rtype: dict
    :raises IOError: if the file is not found
    :raises FileContentError: if there is a problem parsing JSON
    """
    with open(file_name, 'r') as f:
        try:
            content = json.load(f)
        except ValueError as e:
            raise FileContentError(file_name, e)
        return content


class FileContentError(Exception):
    """Problem with file content."""

    def __init__(self, filename, exception=None):
        """Create error.

        :param filename: File name
        :type value: str or unicode
        :param exception: Exception
        :type value: Exception
        """
        super(FileContentError, self).__init__()
        self._filename = filename
        self._exception = exception

    def __str__(self):
        """Get error as a formatted string.

        :return: formatted string
        :rtype: str or unicode
        """
        message = self._filename
        if self._exception is not None:
            message += " : " + str(self._exception)
        return repr(message)

    @property
    def filename(self):
        """Get file name.

        :return: file name
        :rtype: str or unicode
        """
        return self._filename

    @property
    def exception(self):
        """Get exception.

        :param exception: Exception
        :type value: Exception
        """
        return self._exception
import sys
print(load_file(sys.argv[1]))
