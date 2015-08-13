import sys
from .PatchImporter import PatchImporter
import wrapt

from .log import *
from .utils import *

CONFIG = open_config_file()

class PatchSimple(PatchImporter):
    def patch(self, mod):
        for f in self.input_functions:
            if option(CONFIG, 'general', 'debug'):
                print('Patching input function: %s' % f)
            patch_function(mod, f, self.input_wrapper)

        for f in self.output_functions:
            if option(CONFIG, 'general', 'debug'):
                print('Patching output function: %s' % f)
            patch_function(mod, f, self.output_wrapper) 
        return mod