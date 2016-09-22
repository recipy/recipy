"""
Functions to execute commands via the operating system.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

from subprocess import call, check_output, CalledProcessError, STDOUT


def execute(command, arguments, stdout=None, stderr=None):
    """
    Run a command via the operating system.

    :param command: Command to run
    :type command: str or unicode
    :param arguments: Arguments to the command
    :type arguments: list of str or unicode
    :param stdout: File for standard output stream
    :type stdout: file
    :param stderr: File for standard error stream
    :type stderr: file
    :return: exit code
    :rtype: int
    :raises OSError: if there are problems running the command
    """
    command_line = [command]
    command_line.extend(arguments)
    print((" ".join(command_line)))
    return_code = call(command_line, stdout=stdout, stderr=stderr)
    return return_code


def execute_and_capture(command, arguments):
    """
    Run a command via the operating system and capture and return
    standard output and standard error.

    :param command: Command to run
    :type command: str or unicode
    :param arguments: Arguments to the command
    :type arguments: list of str or unicode
    :return: (exit code, standard output and error)
    :rtype: (int, str or unicode)
    :raises OSError: if there are problems running the command
    """
    command_line = [command]
    command_line.extend(arguments)
    print((" ".join(command_line)))
    try:
        result = check_output(command_line, stderr=STDOUT)
        return (0, str(result))
    except CalledProcessError as error:
        return (error.returncode, str(error.output))
