import sys
from .PatchImporter import PatchImporter
import wrapt
import imp

from .log import *
from recipyCommon.utils import *
from recipyCommon.config import option_set

class PatchSimple(PatchImporter):
    """Simple sublass of PatchImporter which implements
    a simple `patch` method that just patches specific input
    and output functions, as specified in the attributes of the class.

    This should not be used directly, but subclasses which set these attributes
    should be created.
    """
    def __init__(self):
        pass
        #if self.modulename in sys.modules:
        #    del sys.modules[self.modulename]

        #    fp, pathname, description = imp.find_module(self.modulename)
        #    print(pathname)
        #    print(description)

        #    try:
        #        imp.load_module(self.modulename, fp, pathname, description)
        #        print('Loaded %s' % self.modulename)
        #    finally:
                # Since we may exit via an exception, close fp explicitly.
        #        if fp:
        #            fp.close()

    def patch(self, mod):
        """Do the patching of `input_functions` and `output_functions`
        in `mod` using `input_wrapper` and `output_wrapper` respectively.
        """
        if not self._ignore_input():
            for f in self.input_functions:
                if option_set('general', 'debug'):
                    print('Patching input function: %s' % f)
                patch_function(mod, f, self.input_wrapper)
        else:
            if option_set('general', 'debug'):
                    print('Ignoring inputs for: %s' % self.modulename)

        if not self._ignore_output():
            for f in self.output_functions:
                if option_set('general', 'debug'):
                    print('Patching output function: %s' % f)
                patch_function(mod, f, self.output_wrapper)
        else:
            if option_set('general', 'debug'):
                    print('Ignoring outputs for: %s' % self.modulename)

        return mod

    def _ignore_input(self):
        root_modulename = self.modulename.split('.')[0]

        return option_set('ignored inputs', root_modulename) or option_set('ignored inputs', 'all')

    def _ignore_output(self):
        root_modulename = self.modulename.split('.')[0]

        return option_set('ignored outputs', root_modulename) or option_set('ignored outputs', 'all')
