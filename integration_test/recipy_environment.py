"""
Functions to access information about recipy's environment.
"""

# Copyright (c) 2015-2016 University of Edinburgh and
# University of Southampton.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import os
import os.path
from .environment import get_home_dir

RECIPYDIR = ".recipy"
RECIPYRC = "recipyrc"
DOTRECIPYRC = "." + RECIPYRC
RECIPYDB = "recipyDB.json"


def get_recipy_dir():
    """
    Get default recipy directory.

    :return: default recipy directory.
    :rtype: str or unicode
    """
    return os.path.expanduser(os.path.join(get_home_dir(), RECIPYDIR))


def get_recipydb():
    """
    Get default recipy database file.

    :return: default recipy database file.
    :rtype: str or unicode
    """
    return os.path.join(get_recipy_dir(), RECIPYDB)


def get_recipyrc():
    """
    Get default recipy configuration file.

    :return: default recipy configuration file
    :rtype: str or unicode
    """
    return os.path.join(get_recipy_dir(), RECIPYRC)


def get_local_recipyrc():
    """
    Get local recipy configuration file.

    :return: local .recipy configuration file
    :rtype: str or unicode
    """
    return os.path.join(os.getcwd(), RECIPYRC)


def get_local_dotrecipyrc():
    """
    Get local .recipy configuration file.

    :return: local .recipy configuration file
    :rtype: str or unicode
    """
    return os.path.join(os.getcwd(), DOTRECIPYRC)
