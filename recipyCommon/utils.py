import wrapt
import imp
import os
import warnings
from datetime import datetime

from tinydb import TinyDB
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


def create_argument_wrapper(log_input_function, log_output_function, arg_loc,
                            kwarg_name, input_values, output_values,
                            default_value, source):
    """Determines how an argument should be logged based on another argument.

    Used in combination with PatchFileOpenLike.

    For example, a netcdf file can be opened using:
    `netCDF4.Dataset(file_name, mode='r')` and written using:
    `netCDF4.Dataset(file_name, mode='w')`. The method named for opening and
    saving are the same. So, this wrapper determines whether a file should be
    logged as an input or as an output, based in the `mode` keyword argument.

    Args:
        log_input_function (function): Log function that should be called if
            the file name refers to an input.
        log_output_function (function): Log function that should be called if
            the file name refers to an output.
        arg_loc (int): index of the file name in the functions' argument list.
        kwarg_name (str):key of the keyword argument that should be used to
            determine whether the file is an input or an output.
        input_values (str or list): values of `kwarg_name` for which the file
            ame should be logged as an input.
        output_values (string or list): values of `kwarg_name` for which the
            file name should be logged as an output.
        default_value (str): value for `kwarg_name` that should be used if
            `kwarg_name` is not set.
        source (str): name of the module that defines the function that is
            wrapped (is currently not used).

    The wrapper for netCDF4 looks like:

    ```
    wrapper = create_argument_wrapper(log_input, log_output, 0, 'mode', 'ra',
                                      'aw', 'r', 'netCDF4')
    ```

    Returns:
        function: wrapped function that logs inputs and outputs when it is
            called.
    """
    @wrapt.decorator
    def f(self, wrapped, instance, args, kwargs):
        val = kwargs.get(kwarg_name, default_value)
        if val in input_values:
            log_input_function(args[arg_loc], source)
        if val in output_values:
            log_output_function(args[arg_loc], source)
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
