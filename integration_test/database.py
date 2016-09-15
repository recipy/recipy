"""
Functions to query the recipy database.
"""

# Copyright (c) 2015-2016 University of Edinburgh and
# University of Southampton.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import json
from tinydb import TinyDB, where, Query


def open(connection):
    """
    Open a connection to a database. The connection is a dictionary of
    information which is database-specific.
    This function looks for a TinyDB file path, with key "tinydb_path".

    :param connection: Database file path
    :type connection: dict
    :return: Database connection
    :rtype: TODO
    :raises: KeyError if tinydb_path is not in connection
    :raises: TODO if the path does not exist
    """
    ## TODO Is use of serializer needed? We're only reading the database.
    # db = TinyDB(connection, storage=tinydb_utils.serializer)
    db = TinyDB(connection["tinydb_path"])
    return db


def get_latest_id(db):
    """
    Get the ID of the most recent log.

    :param db: Database connection
    :type db: TODO
    :return: log ID or None if none
    :rtype: str or unicode
    """
    results = db.all()
    if len(results) == 0:
        return None
    # TODO recipyCmd/recipycmd.py does:
    # results = [get_tinydatestr_as_date(result) for result in results]
    # stripping out '{TinyDate}:' which seems redundant since the sort is
    # still done by string.
    results = sorted(results, key=lambda x: x['date'])
    run = results[-1]
    return run["unique_id"]


def get_log(db, id):
    """
    Get the log with the given ID as a dictionary.

    :param db: Database connection
    :type db: TODO
    :param id: log ID
    :type id: str or unicode
    :return: log or None if no log exists with the given ID.
    :rtype: dict
    """
    results = db.search(where('unique_id').matches(id))
    if len(results) > 0:
        return results[0]
    else:
        return None


def number_of_logs(db):
    """
    Get the number of logs in the database.

    :param db: Database connection
    :type db: TODO
    :return: Number of logs
    :rtype: int
    """
    return len(db.all())


def close(db):
    """
    Close the connection to the database.

    :param db: Database connection
    :type db: TODO
    :raises: TODO if any problems arise
    """
    db.close()

class DatabaseError(Exception):
    # TODO
    def __init__(self):
        pass

conx = {}
conx["tinydb_path"] = "C:/Users/mjj/.recipy/recipyDB.json"
db = open(conx)
print(number_of_logs(db))
id = get_latest_id(db)
print(id)
log = get_log(db, id)
print(log)
close(db)
