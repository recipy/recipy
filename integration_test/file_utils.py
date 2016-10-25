"""
File utilities.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import json
import yaml


def load_yaml(file_name):
    """Load the contents of a YAML file.

    :param file_name: File name
    :type file_name: str or unicode
    :return: content (list of dictionaries, one per YAML document
    in the file) or None if file is empty
    :rtype: list of dict
    :raises IOError: if the file is not found
    :raises FileContentError: if there is a problem parsing YAML
    """
    with open(file_name, 'r') as f:
        try:
            content = [data for data in yaml.load_all(f)]
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
