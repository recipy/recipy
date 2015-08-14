import sys
from .PatchImporter import PatchImporter
from .PatchSimple import PatchSimple

from .log import *
from .utils import *

class PatchGDAL(PatchSimple):
    modulename = 'gdal'

    input_functions = ['Open']
    output_functions = ['Driver.Create', 'Driver.CreateCopy']

    input_wrapper = create_wrapper(log_input, 0, 'gdal')
    output_wrapper = create_wrapper(log_output, 0, 'gdal')

class PatchSKLearn(PatchSimple):
    modulename = 'sklearn'

    input_functions = ['datasets.load_svmlight_file']
    output_functions = ['datasets.dump_svmlight_file']

    input_wrapper = create_wrapper(log_input, 0, 'sklearn')
    output_wrapper = create_wrapper(log_output, 0, 'sklearn')

class PatchSKImage(PatchSimple):
    modulename = 'skimage'

    input_functions = ['io.imread', 'io.load_sift', 'io.load_surf', 'external.tifffile.imread']
    output_functions = ['io.imsave', 'external.tifffile.imsave']

    input_wrapper = create_wrapper(log_input, 0, 'sklearn')
    output_wrapper = create_wrapper(log_output, 0, 'sklearn')

class PatchPillow(PatchSimple):
    modulename = 'skimage'

    input_functions = ['Image.open']
    output_functions = ['Image.save']

    input_wrapper = create_wrapper(log_input, 0, 'Pillow')
    output_wrapper = create_wrapper(log_output, 0, 'Pillow')


multiple_insert(sys.meta_path, [PatchGDAL(), PatchSKLearn(), PatchSKImage(),
                 PatchPillow()])