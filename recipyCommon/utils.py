import wrapt
import imp
import os

from tinydb import TinyDB
from .tinydb_serialization import serialization

from .config import get_db_path


def open_or_create_db(path=get_db_path()):
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))

    db = TinyDB(path, storage=serialization)

    return db

def multiple_insert(lst, items):
    for item in items:
        lst.insert(0, item)

def recursive_getattr(obj, attr):
    prev_part = obj

    for part in attr.split("."):
        prev_part = getattr(prev_part, part)

    return prev_part

def recursive_setattr(obj, attr, value):
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

