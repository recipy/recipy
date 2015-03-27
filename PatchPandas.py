import sys
from PatchImporter import PatchImporter
from PatchSimple import PatchSimple
import wrapt

from log import *
from utils import *

class PatchPandas(PatchSimple):
    input_functions = ['read_csv', 'read_table', 'read_excel', 'read_hdf', 'read_pickle', 'read_stata']
    output_functions = ['DataFrame.to_csv']

    input_wrapper = create_wrapper(log_input, 0, 'pandas')
    output_wrapper = create_wrapper(log_output, 0, 'pandas')

sys.meta_path = [PatchPandas()]