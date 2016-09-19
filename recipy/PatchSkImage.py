from .PatchVerySimple import PatchVerySimple

PatchSKImageIO = PatchVerySimple(modulename='skimage.io',
                                 input_functions=['imread', 'load_sift', 'load_surf'],
                                 output_functions=['imsave'])
