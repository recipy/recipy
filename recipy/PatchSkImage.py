from .PatchVerySimple import PatchVerySimple

PatchSKImageIO = PatchVerySimple(modulename='skimage.io',
                                 input_functions=['imread', 'load_sift', 'load_surf'],
                                 output_functions=['imsave'])

PatchPillow = PatchVerySimple(modulename='PIL.Image',
                              input_functions=['open'])

PatchPillow2 = PatchVerySimple(modulename='PIL.TiffImagePlugin',
                               output_functions=['TiffImageFile.save'])
