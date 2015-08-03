import sys
from .PatchImporter import PatchImporter
import wrapt

from .log import *
from .utils import *

class PatchSimple(PatchImporter):
    def patch(self, mod):
        for f in self.input_functions:
            patch_function(mod, f, self.input_wrapper)

        for f in self.output_functions:
            patch_function(mod, f, self.output_wrapper) 
        return mod