import sys
from .PatchSimple import PatchSimple

from .log import log_input, log_output, add_module_to_db
from recipyCommon.utils import create_wrapper, multiple_insert


class PatchGDAL(PatchSimple):
    modulename = 'gdal'

    input_functions = ['Open']
    output_functions = ['Driver.Create', 'Driver.CreateCopy']

    input_wrapper = create_wrapper(log_input, 0, 'gdal')
    output_wrapper = create_wrapper(log_output, 0, 'gdal')

    add_module_to_db(modulename, input_functions, output_functions)


# class PatchSKLearn(PatchSimple):
#     modulename = 'sklearn'

#     input_functions = ['datasets.load_svmlight_file']
#     output_functions = ['datasets.dump_svmlight_file']

#     input_wrapper = create_wrapper(log_input, 0, 'sklearn')
#     output_wrapper = create_wrapper(log_output, 0, 'sklearn')

#     add_module_to_db(modulename, input_functions, output_functions)

# class PatchSKImage(PatchSimple):
#     modulename = 'skimage'

#     input_functions = ['io.imread', 'io.load_sift', 'io.load_surf', 'external.tifffile.imread']
#     output_functions = ['io.imsave', 'external.tifffile.imsave']

#     input_wrapper = create_wrapper(log_input, 0, 'skimage')
#     output_wrapper = create_wrapper(log_output, 0, 'skimage')

# class PatchPillow(PatchSimple):
#     modulename = 'PIL'

#     input_functions = ['Image.open']
#     output_functions = ['Image.save']

#     input_wrapper = create_wrapper(log_input, 0, 'Pillow')
#     output_wrapper = create_wrapper(log_output, 0, 'Pillow')


class PatchNIBabel(PatchSimple):
    modulename = 'nibabel'

    images = ['nifti1.Nifti1Image', 'nifti2.Nifti2Image', 'freesurfer.mghformat.MGHImage',
              'spm99analyze.Spm99AnalyzeImage', 'minc1.Minc1Image', 'minc2.Minc2Image',
              'analyze.AnalyzeImage', 'parrec.PARRECImage', 'spm2analyze.Spm2AnalyzeImage']

    input_functions = [image_name + '.from_filename' for image_name in images]
    output_functions = [image_name + '.to_filename' for image_name in images]

    input_wrapper = create_wrapper(log_input, 0, 'nibabel')
    output_wrapper = create_wrapper(log_output, 0, 'nibabel')

    add_module_to_db(modulename, input_functions, output_functions)


class PatchTifffile(PatchSimple):
    modulename = 'tifffile'

    input_functions = ['imread']
    output_functions = ['imsave']

    input_wrapper = create_wrapper(log_input, 0, 'tifffile')
    output_wrapper = create_wrapper(log_output, 0, 'tifffile')

class PatchImageio(PatchSimple):
    modulename = 'imageio'

    input_functions = ['core.functions.get_reader', 'core.functions.read']
    output_functions = ['core.functions.get_writer']

    input_wrapper = create_wrapper(log_input, 0, 'imageio')
    output_wrapper = create_wrapper(log_output, 0, 'imageio')

multiple_insert(sys.meta_path, [PatchGDAL(), 
#                                 PatchSKLearn(),
                                PatchNIBabel(), 
                                PatchTifffile(),
                                PatchImageio()])
