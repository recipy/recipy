import wrapt
import imp
import os
from datetime import datetime

from tinydb import TinyDB, where
from .tinydb_utils import serializer

from .config import get_db_path


def open_or_create_db(path=get_db_path()):
    """Get a TinyDB database object for the recipy database.

    This opens the DB, creating it if it doesn't exist.
    """
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))

    db = TinyDB(path, storage=serializer)

    return db


def get_run(db, id=None, latest=False, starts_with=False):
    """Get the runs from db satisfying conditions passed as kwargs.
    If run is unique returns a dict else list of dicts.

    :param id: if provided will match the run id with this value.
    :param latest: if True will return last run.
    :param starts_with: if True and id exists will return all runs starting with id.
    """
    runs = None
    if latest:
        try:
            runs = sorted(db.all(), key=lambda x: x['date'])[-1]
        except (KeyError, IndexError) as _:
            pass

    elif starts_with and id:
        runs = db.search(where('unique_id').matches('{}.*'.format(id)))
        if len(runs) == 1:
            runs = runs[0]

    elif not starts_with and id:
        try:
            runs = db.search(where('unique_id') == id)[0]
        except IndexError:
            pass
    return runs


def _change_date(result):
    result['date'] = str(result['date']).replace('{TinyDate}:', '')
    return result


def reset_patches_table(db_path=get_db_path()):
    db = open_or_create_db(path=db_path)
    patches = db.table('patches')
    patches.purge()
    db.close()


def multiple_insert(lst, items):
    """Inserts all of the items into the list lst"""
    for item in items:
        lst.insert(0, item)


def recursive_getattr(obj, attr):
    """Does the same as the builtin getattr function, but works with multiple sub-attributes.

    So, for example:

    getattr(obj, 'attribute')

    works fine, but

    getattr(obj, 'attribute.anotherattribute')

    doesn't. This fixes that. Use in exactly the same way as getattr.
    """
    prev_part = obj

    for part in attr.split("."):
        prev_part = getattr(prev_part, part)

    return prev_part


def recursive_setattr(obj, attr, value):
    """Does the same as the builtin setattr function, but works with multiple sub-attributes.

    So, for example:

    setattr(obj, 'attribute', value)

    works fine, but

    setattr(obj, 'attribute.anotherattribute', value)

    doesn't. This fixes that. Use in exactly the same way as getattr.
    """
    prev_part = obj

    for part in attr.split(".")[:-1]:
        prev_part = getattr(prev_part, part)

    setattr(prev_part, attr.split(".")[-1], value)


def patch_function(mod, function, wrapper):
        old_f_name = '_%s' % function.replace(".", "_")
        setattr(mod, old_f_name, recursive_getattr(mod, function))

        recursive_setattr(mod, function, wrapper(getattr(mod, old_f_name)))


def create_wrapper(function, arg_loc, source):
    @wrapt.decorator
    def f(self, wrapped, instance, args, kwargs):
        function(args[arg_loc], source)
        return wrapped(*args, **kwargs)

    return f


def recursive_find_module(name, path):
    subnames = name.split(".")
    #print subnames
    #print path
    for subname in subnames[:-1]:
        #print subname
        file_obj, pathname, desc = imp.find_module(subname, path)
        #print subname, file_obj, pathname, desc
        try:
            mod = imp.load_module(subname, file_obj, pathname, desc)
            path = mod.__path__
        finally:
            if file_obj:
                file_obj.close()

    return imp.find_module(subnames[-1], path)


def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        # Serialize datetime as the ISO formatted string
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")
