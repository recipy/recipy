import sys
import warnings


def get_version(modulename):
    "Return a string containing the module name and the library version."
    version = '?'

    if len(modulename.split('.')) > 1:
        modulename = modulename.split('.')[0]

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

    return u'{} v{}'.format(modulename, version)
