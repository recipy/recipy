import sys
import warnings
import numbers

import six


def get_version(modulename):
    "Return a string containing the module name and the library version."
    version = '?'

    # Get the root module name (in case we have something like `recipy.open`
    # or `matplotlib.pyplot`)
    modulename = modulename.split('.')[0]

    if modulename in sys.modules:
        mod = sys.modules[modulename]

        try:
            version = mod.__version__
        except (AttributeError, TypeError, KeyError):
            pass

        try:
            version = mod.version
        except (AttributeError, TypeError, KeyError):
            pass

        try:
            version = mod.version.version
        except (AttributeError, TypeError, KeyError):
            pass

        try:
            version = mod.VERSION
        except (AttributeError, TypeError, KeyError):
            pass

        try:
            version = mod.version()
        except (AttributeError, TypeError, KeyError):
            pass
    else:
        warnings.warn('requesting version of a module that has not been '
                      'imported ({})'.format(modulename))

    # If we get some kind of crazy object (ie. not a string or a number)
    # then ignore it
    if not isinstance(version, (six.string_types, numbers.Number)):
        version = '?'

    return '{} v{}'.format(modulename, version)
