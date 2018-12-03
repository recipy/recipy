################################
Patched Modules
################################

This table lists the modules recipy has patches for, and the input and output
functions that are patched.

Are you missing a patch for your favourite Python package? Learn how to
`create a new patch <#Creating Patches>`_. We are looking forward to your pull request!

=====================  =================================================  ===============================================
modulename             input_functions                                    output_functions
=====================  =================================================  ===============================================
``pandas``             ``read_csv``,                                      ``DataFrame.to_csv``,
                       ``read_table``,                                    ``DataFrame.to_excel``,
                       ``read_excel``,                                    ``DataFrame.to_hdf``,
                       ``read_hdf``,                                      ``DataFrame.to_msgpack``,
                       ``read_pickle``,                                   ``DataFrame.to_stata``,
                       ``read_stata``,                                    ``DataFrame.to_pickle``,
                       ``read_msgpack``                                   ``Panel.to_excel``,
                                                                          ``Panel.to_hdf``,
                                                                          ``Panel.to_msgpack``,
                                                                          ``Panel.to_pickle``,
                                                                          ``Series.to_csv``,
                                                                          ``Series.to_hdf``,
                                                                          ``Series.to_msgpack``,
                                                                          ``Series.to_pickle``
``matplotlib.pyplot``                                                     ``savefig``
``numpy``              ``genfromtxt``,                                    ``save``,
                       ``loadtxt``,                                       ``savez``,
                       ``fromfile``                                       ``savez_compressed``,
                                                                          ``savetxt``
``lxml.etree``         ``parse``,
                       ``iterparse``
``bs4``                ``BeautifulSoup``
``gdal``               ``Open``                                           ``Driver.Create``,
                                                                          ``Driver.CreateCopy``
``sklearn``            ``datasets.load_svmlight_file``                    ``datasets.dump_svmlight_file``
``nibabel``            ``nifti1.Nifti1Image.from_filename``,              ``nifti1.Nifti1Image.to_filename``,
                       ``nifti2.Nifti2Image.from_filename``,              ``nifti2.Nifti2Image.to_filename``,
                       ``freesurfer.mghformat.MGHImage.from_filename``,   ``freesurfer.mghformat.MGHImage.to_filename``,
                       ``spm99analyze.Spm99AnalyzeImage.from_filename``,  ``spm99analyze.Spm99AnalyzeImage.to_filename``,
                       ``minc1.Minc1Image.from_filename``,                ``minc1.Minc1Image.to_filename``,
                       ``minc2.Minc2Image.from_filename``,                ``minc2.Minc2Image.to_filename``,
                       ``analyze.AnalyzeImage.from_filename``,            ``analyze.AnalyzeImage.to_filename``,
                       ``parrec.PARRECImage.from_filename``,              ``parrec.PARRECImage.to_filename``,
                       ``spm2analyze.Spm2AnalyzeImage.from_filename``     ``spm2analyze.Spm2AnalyzeImage.to_filename``
``tifffile``           ``imread``                                         ``imsave``
``imageio``            ``core.functions.get_reader``,                     ``core.functions.get_writer``
                       ``core.functions.read``
``netCDF4``            ``Dataset``                                        ``Dataset``
``xarray``             ``open_dataset``,                                  ``Dataset.to_netcdf``,
                       ``open_mfdataset``,                                ``DataArray.to_netcdf``
                       ``open_rasterio``,
                       ``open_dataarray``
``iris``               ``iris.load``,                                     ``iris.save``
                       ``iris.load_cube``,
                       ``iris.load_cubes``,
                       ``iris.load_raw``
=====================  =================================================  ===============================================

To generate this table do:

.. code-block:: sh

   recipy pm --format rst
