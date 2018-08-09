import six

from .PatchImporter import PatchImporter

from recipyCommon.utils import patch_function, create_wrapper
from recipyCommon.config import option_set


class PatchMultipleWrappers(PatchImporter):
    """Sublass of PatchImporter that allows patching input and output functions
    using more than two wrappers.

    This class should not be used directly, but subclasses which set the
    following class attributes should be created:

    * modulename (str)
    * wrappers (WrapperList)
    """
    def patch(self, mod):
        """Do the patching of `input_functions` and `output_functions`
        in `mod` using `input_wrapper` and `output_wrapper` respectively.
        """
        for f in self.wrappers.functions:
            if not self._ignore(f):
                if option_set('general', 'debug'):
                    msg = 'Patching {} function: {}'.format(f['type'],
                                                            f['function'])
                    print(msg)
                # The function that is returned by create_wrapper assumes that
                # the wrapper is created directly on the patch object (the
                # first argument of f is self). We have to fake that here.
                # Otherwise, there will be an error, because an argument is
                # missing:
                # TypeError f() takes exactly 5 arguments (4 given)
                setattr(self.__class__, 'wrapper', f['wrapper'])
                patch_function(mod, f['function'], self.wrapper)
            else:
                if option_set('general', 'debug'):
                    print('Ignoring {} for: {}'.format(f['type'],
                                                       self.modulename))

        return mod

    def _ignore(self, f):
        root_modulename = self.modulename.split('.')[0]

        opt = 'ignored {}s'.format(f['type'])

        return option_set(opt, root_modulename) or option_set(opt, 'all')


class WrapperList(object):
    """A store for functions and their wrappers.
    """
    def __init__(self):
        self.functions = []

    def add(self, function_names, log_function, arg_loc, modname,
            function_type):
        if isinstance(function_names, six.string_types):
            function_names = [function_names]

        wrapper = create_wrapper(log_function, arg_loc, modname)
        for f in function_names:
            self.functions.append({'function': f,
                                   'wrapper': wrapper,
                                   'type': function_type})

    def add_inputs(self, function_names, log_function, arg_loc, modname):
        return self.add(function_names, log_function, arg_loc, modname,
                        'input')

    def add_outputs(self, function_names, log_function, arg_loc, modname):
        return self.add(function_names, log_function, arg_loc, modname,
                        'output')
