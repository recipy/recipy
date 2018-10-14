
Package versioning problems
===========================

The sample scripts in ``integration_tests/packages`` may fail to run
with older versions of third-party packages. Known package versions
that can cause failures are listed below.

These can arise due to differences in versions of packages (especially
their APIs) installed by ``conda``\ , ``pip``\ , ``easy_install`` or within
Python-related packages installed via ``apt-get`` or ``yum`` under Linux.

NiBabel ``AttributeError``
------------------------------

.. code-block:: console

   $ python -m integration_test.packages.run_nibabel nifti2_from_filename
       data = nib.Nifti2Image.from_filename(file_name)
   AttributeError: 'module' object has no attribute 'Nifti2Image'

   $ python -m integration_test.packages.run_nibabel nifti2_to_filename
       img = nib.Nifti2Image(self.get_data(), self,get_affine())
   AttributeError: 'module' object has no attribute 'Nifti2Image'

   $ python -m integration_test.packages.run_nibabel minc1_from_filename
       data = nib.minc1.Minc1Image.from_filename(file_name)
   AttributeError: 'module' object has no attribute 'minc1'

   $ python -m integration_test.packages.run_nibabel minc1_to_filename
       img = nib.minc1.Minc1Image(self.get_data(), np.eye(4))
   AttributeError: 'module' object has no attribute 'minc1'

   $ python -m integration_test.packages.run_nibabel minc2_from_filename
       data = nib.minc2.Minc2Image.from_filename(file_name)
   AttributeError: 'module' object has no attribute 'minc2'

   $ python -m integration_test.packages.run_nibabel minc2_to_filename
       img = nib.minc2.Minc2Image(self.get_data(), np.eye(4))
   AttributeError: 'module' object has no attribute 'minc2'

   $ python -m integration_test.packages.run_nibabel parrec_from_filename
       data = nib.parrec.PARRECImage.from_filename(file_name)
   AttributeError: 'module' object has no attribute 'parrec'

   $ python -m integration_test.packages.run_nibabel parrec_to_filename
       img = nib.parrec.PARRECImage.from_filename(file_name)
   AttributeError: 'module' object has no attribute 'parrec'
   `

Fails on nibabel 1.2.2 (bundled in Ubuntu package ``python-nibabel``\ )
due to change in package API.

Succeeds on 2.0.2.

PIL ``AttributeError``
--------------------------

.. code-block:: console

   $ python -m integration_test.packages.run_pil image_open
     File "/usr/lib/python2.7/dist-packages/PIL/Image.py", line 528, in __getattr__
       raise AttributeError(name)
   AttributeError: __exit__

   $ python -m integration_test.packages.run_pil image_save
   ...as above...

Fails on PIL/pillow 2.3.0 (bundled in Ubuntu package ``python-pillow``\ )
due to change in package API.

Succeeds on 3.2.0+.

pandas ``TypeError``
------------------------

.. code-block:: console

   $ python -m integration_test.packages.run_pandas read_excel
   TypeError: read_excel() takes exactly 2 arguments (1 given)

   $ python3 -m integration_test.packages.run_pandas read_excel
   TypeError: read_excel() missing 1 required positional argument: 'sheetname'

   $ python -m integration_test.packages.run_pandas read_hdf
   TypeError: read_hdf() takes exactly 2 arguments (1 given)

   $ python3 -m integration_test.packages.run_pandas read_hdf
   TypeError: read_hdf() missing 1 required positional argument: 'key'

Fails on pandas 0.13.1 (bundled in Ubuntu package ``python-pandas``\ ) due
to change in package API.

Succeeds on 0.18.1.

pandas ``ImportError``
--------------------------

.. code-block:: console

   $ python -m integration_test.packages.run_pandas read_pickle
   ImportError: No module named indexes.base

   $ python3 -m integration_test.packages.run_pandas read_pickle
   ImportError: No module named 'pandas.indexes'

   During handling of the above exception, another exception occurred:
   ...

Fails on pandas 0.13.1 (bundled in Ubuntu package ``python-pandas``\ ) due
to change in package API.

Succeeds on 0.18.1.

pandas ``ValueError``
-------------------------

.. code-block:: console

   $ python -m integration_test.packages.run_pandas read_msgpack
   ValueError: Unpack failed: error = -1

   $ python3 -m integration_test.packages.run_pandas read_msgpack
   ...as above...

Fails on pandas 0.13.1 (bundled in Ubuntu package ``python-pandas``\ ) due
to change in file format. The scripts work if run using data files
created by pandas 0.13.1.

Succeeds on 0.18.1.

skimage ``NameError``
-------------------------

.. code-block:: console

   $ python -m integration_test.packages.run_skimage io_load_sift
   NameError: name 'file' is not defined

   $ python -m integration_test.packages.run_skimage io_load_surf
   NameError: name 'file' is not defined

Fails on Python 3 as ``file()`` built-in removed in Python -M
Integration_Test.Packages.3 (see
`Builtins <https://docs.python.org/release/3.0/whatsnew/3.0.html#builtins>`_\ ).

skimage ``ImportError``
---------------------------

``run_skimage.py`` examples fail with:

.. code-block:: console

   Traceback (most recent call last):
     File "run_skimage.py", line 13, in <module>
       from skimage import external
   ImportError: cannot import name 'external'

Commenting out:

.. code-block:: console

   from skimage import external

allows non-external.tifffile examples to run.

Fails on skimage 0.9.3 (bundled in Ubuntu package ``python-skimage``\ )
due to change in package API.

Succeeds on 0.12.3.
