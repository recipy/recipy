"""
Functions to access information about the execution environment.
"""

# Copyright (c) 2015-2016 University of Edinburgh and
# University of Southampton.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import getpass
import os.path
import platform
import sys
import pip
from dateutil.parser import parse


def get_str_as_date(date_str):
    """
    Convert string to date object.

    :param date_str: Date string e.g. '2016-09-12T09:40:20'
    :type date_str: str or unicode
    :return: date
    :rtype: datetime.datetime
    """
    return parse(date_str)


def get_tinydatestr_as_date(date_str):
    """
    Convert TinyDate string to date object.

    :param date_str: Date string e.g. '{TinyDate}:2016-09-12T09:40:20'
    :type date_str: str or unicode
    :return: date
    :rtype: datetime.datetime
    """
    return parse(date_str.replace('{TinyDate}:', ''))


def get_user():
    """
    Get current user.

    :return: current user
    :rtype: str or unicode
    """
    return getpass.getuser()


def get_python_exe():
    """
    Get Python executable path.

    :return: Python executable path
    :rtype: str or unicode
    """
    return sys.executable


def get_python_version():
    """
    Get Python version.

    :return: Python version
    :rtype: str or unicode
    """
    return sys.version.split("\n")[0]


def get_os():
    """
    Get operating system.

    :return: operating system
    :rtype: str or unicode
    """
    return platform.platform()


def is_package_installed(packages, package):
    """
    Is a package installed?

    :param packages: installed packages and versions, keyed by package
    name
    :type packages: dict of str or unicode => str or unicode
    :param package: Package name
    :type package: str or unicode
    :return: True if it is installed, False otherwise
    :rtype: bool
    """
    return package in packages


def get_package_version(packages, package):
    """
    Get version of installed package.

    :param packages: installed packages and versions, keyed by package
    name
    :type packages: dict of str or unicode => str or unicode
    :param package: Package name
    :type package: str or unicode
    :return: Package version
    :rtype: str or unicode
    :raises KeyError: if the package is not installed
    """
    return packages[package]


def get_packages():
    """
    Get list of installed packages and their versions.

    :return: installed packages and versions, keyed by package name
    :rtype: dict of str or unicode => str or unicode
    """
    packages = pip.get_installed_distributions(local_only=False)
    packages_dict = {}
    for package in packages:
        packages_dict[package.key] = package.version
    return packages_dict


def get_home_dir():
    """
    Get home directory.

    :return: home directory
    :rtype: str or unicode
    """
    return os.path.expanduser("~")
