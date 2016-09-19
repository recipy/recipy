import sys

from .PatchSimple import PatchSimple

from .log import log_input, log_output, add_module_to_db
from recipyCommon.utils import create_wrapper_simple


class PatchVerySimple(PatchSimple):

    def __init__(self, modulename, input_functions=[], output_functions=[],
                 input_wrapper=None, output_wrapper=None):
        self.modulename = modulename

        self.input_functions = input_functions

        self.output_functions = output_functions

        if input_wrapper is None:
            self.input_wrapper = create_wrapper_simple(log_input, 0, modulename)
        else:
            self.input_wrapper = input_wrapper

        if output_wrapper is None:
            self.output_wrapper = create_wrapper_simple(log_output, 0, modulename)
        else:
            self.output_wrapper = output_wrapper

        add_module_to_db(modulename, input_functions, output_functions)

        sys.meta_path.insert(0, self)
