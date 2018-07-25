import sys
import pkg_resources
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
        ws = pkg_resources.working_set
        package = ws.find(pkg_resources.Requirement(modulename))
        version = package.version
    else:
        warnings.warn('requesting version of a module that has not been '
                      'imported ({})'.format(modulename))

    # If we get some kind of crazy object (ie. not a string or a number)
    # then ignore it
    if not isinstance(version, (six.string_types, numbers.Number)):
        version = '?'

    return '{} v{}'.format(modulename, version)
