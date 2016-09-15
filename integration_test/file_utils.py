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
    :raises IOError: if the file is not found or does not contain a
    valid YAML or JSON document
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
    :return: content
    :rtype: dict
    :raises IOError: if the file is not found or does not contain a
    valid YAML document
    """
    with open(file_name, 'r') as f:
        try:
            content = yaml.load(f)
        except yaml.scanner.ScannerError as e:
            raise IOError(0, "Content is not valid YAML", file_name)
        if type(content) is not dict:
            raise IOError(0, "Content is not valid YAML", file_name)
    return content


def load_json(file_name):
    """Load the contents of a JSON file.
  
    :param file_name: File name
    :type file_name: str or unicode
    :return: content
    :rtype: dict
    :raises IOError: if the file is not found or does not contain a
    valid JSON document
    """
    with open(file_name, 'r') as f:
        try:
            content = json.load(f)
        except ValueError as e:
            raise IOError(0, "Content is not valid JSON", file_name)
        return content
