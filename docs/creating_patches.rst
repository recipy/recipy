Creating Patches
================

Patches are derived from :class:`~recipy.PatchImporter.PatchImporter`, often
using the easier interface provided by :class:`~recipy.PatchSimple.PatchSimple`.
To create a patch, you need to specify the module name, the input and output
functions, and the argument referencing the file path.

Simple patches
***************

Because most of the complexity is hidden away, the actual code to wrap a module
is fairly simple. Using :class:`~recipy.PatchSimple.PatchSimple`, the patch
for `numpy <http://www.numpy.org>`_ looks like:

.. code-block:: python
  :linenos:

  from .PatchSimple import PatchSimple
  from .log import log_input, log_output, add_module_to_db
  from recipyCommon.utils import create_wrapper

  # Inherit from PatchSimple
  class PatchNumpy(PatchSimple):
    # Specify the full name of the module
    modulename = 'numpy'

    # List functions that are involved in input/output
    # these can be anything that can go after "modulename."
    # so they could be something like "pyplot.savefig" for example
    input_functions = ['genfromtxt', 'loadtxt', 'load', 'fromfile']
    output_functions = ['save', 'savez', 'savez_compressed', 'savetxt']

    # Define the functions that will be used to wrap the input/output
    # functions.
    # In this case we are calling the log_input function to log it to
    # the DB and we are giving it the 0th argument from the function
    # (because all of the functions above take the filename as the
    # 0th argument), and telling it that it came from numpy.
    input_wrapper = create_wrapper(log_input, 0, 'numpy')
    output_wrapper = create_wrapper(log_output, 0, 'numpy')

    # Add the module to the database, so we can list it.
    add_module_to_db(modulename, input_functions, output_functions)

First, we import the required functionality (lines 1-3). In addition to
:class:`~recipy.PatchSimple.PatchSimple`, we need functions that do the actual
logging (:meth:`~recipy.log.log_input` and :meth:`~recipy.log.log_output`),
write details about the module to the database
(:meth:`~recipy.log.add_module_to_db`), and a function to create wrappers
(:meth:`~recipyCommon.utils.create_wrapper`). Next, we define a class
for the patch that inherits from :class:`~recipy.PatchSimple.PatchSimple` (line
6). In this class, we need to define the module name (line 8), and the input and
output functions (line 13 and 14).
Because the patches rely on class attributes, it is important to use the
variable names specified in the example code.
Then, we need to define the input and output
wrapper (line 22 and 23). The wrappers are created using a predefined function,
that needs as inputs a logging function (i.e., :meth:`~recipy.log.log_input`
or :meth:`~recipy.log.log_output`), the index of the argument that specifies
the file path in the input or output function, and the name of the module.
Finally, the module is added to the database (line 26).

Enabling a patch
****************

Patch objects for specific modules can be found in
:mod:`~recipy.PatchBaseScientific` and :mod:`~recipy.PatchScientific`. To enable
a new patch, one more step is required; the constructor of the new object should
be called inside :meth:`~recipyCommon.utils.multiple_insert`. This function is
called at the bottom of :mod:`~recipy.PatchBaseScientific` and
:mod:`~recipy.PatchScientific`.

Patching more complex modules
*****************************

Most of the patched modules are based on :class:`~recipy.PatchSimple.PatchSimple`.
However, some modules require more complexity. Some modules, e.g.,
`netcdf4-python <http://unidata.github.io/netcdf4-python/>`_, use a file open like
method for reading and writing files; the method called is the same, and whether
the file is read or written depends on arguments:

.. code-block:: python
  :linenos:

  from netCDF4 import Dataset

  ds = Dataset('test.nc', 'r')  # read test.nc
  ds = Dataset('test.nc', 'w')  # write test.nc

For this situation a different patch type and wrapper creation function are
available: :class:`~recipy.PatchFileOpenLike` in combination with
:meth:`~recipy.log.create_argument_wrapper`.

The complete code example (:class:`~recipy.PatchNetCDF4`):

.. code-block:: python
  :linenos:

  from .PatchFileOpenLike import PatchFileOpenLike
  from .log import log_input, log_output, add_module_to_db
  from recipyCommon.utils import create_argument_wrapper

  class PatchNetCDF4(PatchFileOpenLike):
    modulename = 'netCDF4'

    functions = ['Dataset']

    wrapper = create_argument_wrapper(log_input, log_output, 0, 'mode', 'ra',
                                      'aw', 'r', 'netCDF4')

    add_module_to_db(modulename, functions, functions)

Another instance where it isn't possible to use
:class:`~recipy.PatchSimple.PatchSimple` is when not all input or output
functions have the file path in the same position. For example,
`xarray <http://xarray.pydata.org/>`_
has three functions for writing files, i.e., :meth:`~xarray.Dataset.to_netcdf`,
:meth:`~xarray.DataArray.to_netcdf`, and :func:`~xarray.save_mfdataset`.
For :meth:`~xarray.Dataset.to_netcdf` and :meth:`~xarray.DataArray.to_netcdf`,
the file paths are argument 0, as in the previous examples. However, the
argument for the file paths of :func:`~xarray.save_mfdataset` (it is a method
for writing multiple files at once) is 1.
With :class:`~recipy.PatchSimple.PatchSimple` there is no way to represent this.

A patch class that allows specifying separate wrappers for different functions
is :class:`~recipy.PatchMultipleWrappers.PatchMultipleWrappers`. Using this
class involves defining a :class:`~recipy.PatchMultipleWrappers.WrapperList` to
which inputs and outputs can be added. As can be seen in the following code
example (:class:`~recipy.PatchXarray`), you can specify a wrapper for a list
of functions (line 13 and 14) or for one function (line 15).

.. code-block:: python
  :linenos:

  from .PatchMultipleWrappers import PatchMultipleWrappers, WrapperList
  from .log import log_input, log_output, add_module_to_db

  class PatchXarray(PatchMultipleWrappers):
    modulename = 'xarray'

    wrappers = WrapperList()

    input_functions = ['open_dataset', 'open_mfdataset', 'open_rasterio',
                       'open_dataarray']
    output_functions = ['Dataset.to_netcdf', 'DataArray.to_netcdf']

    wrappers.add_inputs(input_functions, log_input, 0, modulename)
    wrappers.add_outputs(output_functions, log_output, 0, modulename)
    wrappers.add_outputs('save_mfdataset', log_output, 1, modulename)

    add_module_to_db(modulename, input_functions, output_functions)

Writing tests
*************

If you make a new patch, please include tests (your pull request won't be
accepted without them)! Recipy has a testing framework that checks
whether inputs and outputs are actually logged when a function is called
(see :ref:`Test Framework` for more details).

If you create a patch for a module, follow these steps to create tests:

1. Prepare small data files for testing, and create a directory
   ``integration_test/packages/data/<module name>`` containing these files.

   * Small means kilobytes!

2. Create a test script for the patch. The name of the script
   should be ``run_<module name>.py``.

   * It is probably easiest to copy one of the
     existing scripts in ``integration_test/packages/``, so you can reuse the
     set up (it is pretty self-explanatory).

3. Write a test method for each input/output method.

   * Be sure to add docstrings!

4. Add the test configuration.

   * Open ``integration_test/config/test_packages.yml``
   * Add a new section by typing:

   .. code-block:: sh

     ---
     script: run_<module name>.py
     libraries: [ modulename ]
     test_cases:

   * Add a test case for each method in ``run_<module name>.py``, specifying
     ``arguments``, a list containing the name of the test method,
     ``inputs``, a list of the input files this method needs (if any), and
     ``outputs``, a list of the output files this method  creates (if any):

   .. code-block:: sh

     - arguments: [ <test method name> ]
       inputs: [<input names>]
       outputs: [<output names>]

   * Specified input files should exist in
     ``integration_test/packages/data/<module name>``
   * Test cases can skipped by adding the line: ``skip: "<reason for skipping>"``
   * If you need to skip a test, please add a description of the problem plus
     how to reproduce it in the :ref:`Recipy and Third-Party Package Issues`
     section
   * If a test case should be skipped in certain Python versions, add
     ``skip_py_version: [ <python versions> ]``

5. Run the tests by typing: ``py.test -v integration_test/``
