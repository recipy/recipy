import sys

from .PatchSimple import PatchSimple

from .log import log_input, log_output, add_module_to_db
from recipyCommon.utils import create_wrapper, create_wrapper_simple, multiple_insert

class PatchVerySimple(PatchSimple):

    # input_wrapper = create_wrapper(log_input, 0, 'skimage.io')
    # output_wrapper = create_wrapper(log_output, 0, 'skimage.io')

    def __init__(self, modulename, input_functions, output_functions,
                 input_wrapper=None, output_wrapper=None):
        self.modulename = modulename
        #print(modulename)

        self.input_functions = input_functions

        self.output_functions = output_functions

        self.input_wrapper = create_wrapper_simple(log_input, 0, 'skimage.io')
        self.output_wrapper = create_wrapper_simple(log_output, 0, 'skimage.io')

        add_module_to_db(modulename, input_functions, output_functions)

        sys.meta_path.insert(0, self)
