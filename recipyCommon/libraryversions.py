import sys
import warnings


def get_version(modulename):
    "Return a string containing the module name and the library version."
    version = '?'
    if modulename in sys.modules:
        try:
            version = sys.modules[modulename].__version__
        except:
            pass

        try:
            version = sys.modules[modulename].version
        except:
            pass

        try:
            version = sys.modules[modulename].version.version
        except:
            pass

        try:
            version = sys.modules[modulename].VERSION
        except:
            pass
    else:
        warnings.warn('requesting version of a module that has not been '
                      'imported ({})'.format(modulename))

    return '{} v{}'.format(modulename, version)
