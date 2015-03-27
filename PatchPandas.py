import sys
from patch_generic import PatchImporter
import wrapt

from log import *
from utils import *

class PatchPandas(PatchImporter):

    def patch_function(self, mod, function, wrapper):
        old_f_name = '_%s' % function.replace(".", "_")
        setattr(mod, old_f_name, recursive_getattr(mod, function))

        recursive_setattr(mod, function, wrapper(getattr(mod, old_f_name)))

    def patch(self, mod):
        input_functions = ['read_csv', 'read_table', 'read_excel', 'read_hdf', 'read_pickle', 'read_stata']
        for f in input_functions:
            self.patch_function(mod, f, self.log_pandas_read)

        self.patch_function(mod, 'DataFrame.to_csv', self.log_pandas_write) 
        return mod

    @wrapt.decorator
    def log_pandas_read(self, wrapped, instance, args, kwargs):
        log_input(args[0], 'pandas')
        return wrapped(*args, **kwargs)

    @wrapt.decorator
    def log_pandas_write(self, wrapped, instance, args, kwargs):
        log_output(args[0], 'pandas')
        return wrapped(*args, **kwargs)

sys.meta_path = [PatchPandas()]