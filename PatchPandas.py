import sys
from patch_generic import PatchImporter
import wrapt

from log import *

class PatchPandas(PatchImporter):

    def patch_function(self, mod, function, wrapper):
        setattr(mod, '_%s' % function.__name__, function)
        setattr(mod, function.__name__, wrapper(getattr(mod, '_%s' % function.__name__)))
        # eval("{0}._{1} = {0}.{1}".format(mod, function))
        # #eval("{0}.{1} = {2}")

    def patch(self, mod):
        # mod._read_csv = mod.read_csv
        # mod.read_csv = log_input(mod.read_csv)
        self.patch_function(mod, mod.read_csv, self.log_pandas_read)
        return mod

    @wrapt.decorator
    def log_pandas_read(self, wrapped, instance, args, kwargs):
        log_input(args[0], 'pandas')
        return wrapped(*args, **kwargs)

sys.meta_path = [PatchPandas()]