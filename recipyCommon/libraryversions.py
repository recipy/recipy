import sys
import warnings


def get_version(modulename):
    "Return a string containing the module name and the library version."
    version = '?'

    # Get the root module name (in case we have something like `recipy.open`
    # or `matplotlib.pyplot`)
    modulename = modulename.split('.')[0]

    if modulename in sys.modules:
        try:
            version = sys.modules[modulename].__version__
        except (KeyError, AttributeError):
            pass

        try:
            version = sys.modules[modulename].version
        except (KeyError, AttributeError):
            pass

        try:
            version = sys.modules[modulename].version.version
        except (KeyError, AttributeError):
            pass

        try:
            version = sys.modules[modulename].VERSION
        except (KeyError, AttributeError):
            pass
    else:
        warnings.warn('requesting version of a module that has not been '
                      'imported ({})'.format(modulename))

    return '{} v{}'.format(modulename, version)
