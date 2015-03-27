import sys
from patch_generic import PatchImporter
from log import *

class PatchPandas(PatchImporter):

    def patch(self, mod):
        mod._read_csv = mod.read_csv
        mod.read_csv = log_input(mod.read_csv)
        return mod

sys.meta_path = [PatchPandas()]