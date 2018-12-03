How does it work?
=================

For each run of your script, recipy logs information about which script was run,
the command line arguments, Python version, git or svn repo, warnings, errors,
and inputs and outputs (see :ref:`database_schema` for a complete overview).
Gathering most of this information is straightforward using the Python Standard
Library and specialized packages (such as,
`GitPython <https://gitpython.readthedocs.io/en/stable/>`_
or `svn <https://github.com/dsoprea/PySvn>`_).
Automatically logging inputs and outputs, recipy's most important feature, is
more complicated.

When a Python module that reads or writes files is imported, recipy wraps
methods for reading and writing files to log file paths to the database.
To make this happen, recipy contains a patch for every library that reads or
writes files.  When you import recipy, the patches are added to
:data:`sys.meta_path` so they can be used to wrap a module's functions that read
or write files when it is imported. This is why `import recipy` should be called
before importing other modules.

Currently, recipy contains patches for many popular (scientific) libraries,
including :mod:`numpy` and :mod:`pandas`. For an overview see :ref:`Patched Modules`.
Is your favourite module missing? Have a look at :ref:`Creating Patches`.
We are looking forward to your pull request!
