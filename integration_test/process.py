"""
Functions to execute commands via the operating system.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

from subprocess import call
from tempfile import TemporaryFile


def execute(command, stdout=None, stderr=None):
    """
    Run a command via the operating system.

    :param command: Command to run plus any arguments
    :type command: list of str or unicode
    :param stdout: File for standard output stream
    :type stdout: file
    :param stderr: File for standard error stream
    :type stderr: file
    :return: exit code
    :rtype: int
    :raises OSError: if there are problems running the command
    """
    print((" ".join(command)))
    return_code = call(command, stdout=stdout, stderr=stderr)
    return return_code


def execute_and_capture(command):
    """
    Run a command via the operating system and capture and return
    standard output and standard error.

    :param command: Command to run plus any arguments
    :type command: list of str or unicode
    :return: (exit code, standard output and error)
    :rtype: (int, str or unicode)
    :raises OSError: if there are problems running the command
    """
    with TemporaryFile(mode='w+', suffix="log") as stdouterr:
        result = execute(command, stdout=stdouterr, stderr=stdouterr)
        stdouterr.seek(0)
        log = stdouterr.readlines()
    return (result, log)
