import sys
from patch_generic import PatchImporter
import wrapt

from log import *
from utils import *

class PatchPandas(PatchImporter):
    input_functions = ['read_csv', 'read_table', 'read_excel', 'read_hdf', 'read_pickle', 'read_stata']
    output_functions = ['DataFrame.to_csv']



    def patch(self, mod):
        for f in self.input_functions:
            patch_function(mod, f, create_wrapper(log_input, 0, 'pandas'))

        for f in self.output_functions:
            patch_function(mod, f, create_wrapper(log_output, 0, 'pandas')) 
        return mod


    

    # @wrapt.decorator
    # def log_pandas_write(self, wrapped, instance, args, kwargs):
    #     log_output(args[0], 'pandas')
    #     return wrapped(*args, **kwargs)

sys.meta_path = [PatchPandas()]