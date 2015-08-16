import sys
from .PatchImporter import PatchImporter
import wrapt

from .log import *
from .utils import *

CONFIG = open_config_file()

class PatchSimple(PatchImporter):
    """Simple sublass of PatchImporter which implements
    a simple `patch` method that just patches specific input
    and output functions, as specified in the attributes of the class.

    This should not be used directly, but subclasses which set these attributes
    should be created.
    """

    def patch(self, mod):
        """Do the patching of `input_functions` and `output_functions`
        in `mod` using `input_wrapper` and `output_wrapper` respectively.
        """
        
        for f in self.input_functions:
            if option(CONFIG, 'general', 'debug'):
                print('Patching input function: %s' % f)
            patch_function(mod, f, self.input_wrapper)

        for f in self.output_functions:
            if option(CONFIG, 'general', 'debug'):
                print('Patching output function: %s' % f)
            patch_function(mod, f, self.output_wrapper) 
        return mod