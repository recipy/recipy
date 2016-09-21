"""
Functions to query the recipy database.
"""

# Copyright (c) 2015-2016 University of Edinburgh and
# University of Southampton.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

from tinydb import TinyDB, where


TINYDB_PATH = "tinydb_path"


def open_db(connection):
    """
    Open a connection to a database. The connection is a dictionary of
    information which is database-specific.
    This function looks for a TinyDB file path, with key "tinydb_path".

    :param connection: Database file path
    :type connection: dict
    :return: Database connection
    :rtype: tinydb.database.TinyDB
    :raises DatabaseError if tinydb_path is not in connection
    or if there are other problems in connecting to the database
    """
    try:
        path = connection[TINYDB_PATH]
    except Exception as exception:
        raise DatabaseError("Missing configuration error", exception)
    try:
        database = TinyDB(path)
    except Exception as exception:
        raise DatabaseError("Open connection error", exception)
    return database


def get_latest_id(database):
    """
    Get the ID of the most recent log.

    :param database: Database connection
    :type database: tinydb.database.TinyDB
    :return: log ID or None if none
    :rtype: str or unicode
    :raises DatabaseError if there are problems in connecting to the
    database
    """
    try:
        results = database.all()
    except Exception as exception:
        raise DatabaseError("Query error", exception)
    if len(results) == 0:
        return None
    results = sorted(results, key=lambda x: x['date'])
    run = results[-1]
    return run["unique_id"]


def get_log(database, log_id):
    """
    Get the log with the given ID as a dictionary. The log and the
    log number (the identity of this log in the database) are
    both returned.

    :param database: Database connection
    :type database: tinydb.database.TinyDB
    :param log_id: log ID
    :type log_id: str or unicode
    :return: log number and log, or None if no log exists with
    the given ID.
    :rtype: (int, dict)
    :raises DatabaseError if there are problems in connecting to the
    database
    """
    try:
        results = database.search(where('unique_id').matches(log_id))
    except Exception as exception:
        raise DatabaseError("Query error", exception)
    if len(results) > 0:
        return (results[0].eid, dict(results[0]))
    else:
        return None


def get_filediffs(database, log_number):
    """
    Get the 'filediffs' entry for the log with the given log number.
    The log_number is returned via get_log.

    :param database: Database connection
    :type database: tinydb.database.TinyDB
    :param log_number: log number
    :type log_id: str or unicode
    :return: 'filediffs' entry or None if none
    :rtype: dict
    :raises DatabaseError if there are problems in connecting to the
    database
    """
    try:
        diffs = database.table("filediffs")
        results = diffs.search(where("run_id") == log_number)
    except Exception as exception:
        raise DatabaseError("Query error", exception)
    if len(results) > 0:
        return dict(results[0])
    else:
        return None


def number_of_logs(database):
    """
    Get the number of logs in the database.

    :param database: Database connection
    :type database: tinydb.database.TinyDB
    :return: Number of logs
    :rtype: int
    :raises DatabaseError if there are problems in connecting to the
    database
    """
    try:
        return len(database.all())
    except Exception as exception:
        raise DatabaseError("Query error", exception)


def close_db(database):
    """
    Close the connection to the database.

    :param database: Database connection
    :type database: tinydb.database.TinyDB
    :raises DatabaseError if there are problems in connecting to the
    database
    """
    try:
        database.close()
    except Exception as exception:
        raise DatabaseError("Close connection error", exception)


class DatabaseError(Exception):
    """Problem with using a database."""

    def __init__(self, message, exception=None):
        """Create error.

        :param message: Message
        :type message: str or unicode
        :param exception: Exception
        :type value: Exception
        """
        super(DatabaseError, self).__init__()
        self._message = message
        self._exception = exception

    def __str__(self):
        """Get error as a formatted string.

        :return: formatted string
        :rtype: str or unicode
        """
        message = self._message
        if self._exception is not None:
            message += " : " + str(self._exception)
        return repr(message)

    @property
    def exception(self):
        """Get exception.

        :param exception: Exception
        :type value: Exception
        """
        return self._exception
