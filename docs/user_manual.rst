##########################
User Manual
##########################

With the addition of a single line of code to the top of a Python script, recipy
logs each run of your code to a database, keeping track of the input files, output
files and the version of your code. It then lets you query this database to
help you to recall the exact steps you took to create a certain output file.

Logging Provenance Information
==============================

To log provenance information, simply add the following line to the top of your
code:

.. code-block:: python

   import recipy

Note that this **must** be the **very top** line of your script, before you
import anything else.

Then just run your script as usual, and all of the data will be logged into the
TinyDB database (don't worry, the database is automatically created if needed).
You can then use the ``recipy`` command to quickly query the database to find out
what run of your code produced what output file. So, for example, if you run some
code like this:

.. code-block:: python

   import recipy
   import numpy

   arr = numpy.arange(10)
   arr = arr + 500

   numpy.save('test.npy', arr)

(Note the addition of ``import recipy`` at the beginning of script - but there
are no other changes from a standard script.)

Alternatively, run an unmodified script with ``python -m recipy SCRIPT [ARGS ...]``
to enable recipy logging. This invokes recipy's module entry point, which takes
care of import recipy for you, before running your script.

Retrieving Information about Runs
=================================

it will produce an output called ``test.npy``. To find out the details of the
run which created this file you can search using

.. code-block:: sh

   recipy search test.npy


and it will display information like the following:

.. code-block:: sh

   Created by robin on 2015-05-25 19:00:15.631000
   Ran /Users/robin/code/recipy/example_script.py using /usr/local/opt/python/bin/python2.7
   Git: commit 91a245e5ea82f33ae58380629b6586883cca3ac4, in repo /Users/robin/code/recipy, with origin git@github.com:recipy/recipy.git
   Environment: Darwin-14.3.0-x86_64-i386-64bit, python 2.7.9 (default, Feb 10 2015, 03:28:08)
   Inputs:

   Outputs:
     /Users/robin/code/recipy/test.npy

An alternative way to view this is to use the GUI. Just run ``recipy gui`` and
a browser window will open with an interface that you can use to search all of
your recipy 'runs':

.. image:: http://rtwilson.com/images/RecipyGUI.png
   :target: http://rtwilson.com/images/RecipyGUI.png
   :alt: Screenshot of GUI

Logging Files Using Built-In Open
=================================

If you want to log inputs and outputs of files read or written with built-in
open, you need to do a little more work. Either use ``recipy.open``
(only requires ``import recipy`` at the top of your script), or add
``from recipy import open`` and just use ``open``.

This workaround is required, because many libraries use built-in open internally,
and you only want to record the files you explicitly opened yourself.

If you use Python 2, you can pass an ``encoding`` parameter to ``recipy.open``.
In this case ``codecs`` is used to open the file with proper encoding.

Annotating Runs
===============

Once you've got some runs in your database, you can 'annotate' these runs with
any notes that you want to keep about them. This can be particularly useful for
recording which runs worked well, or particular problems you ran into. This can
be done from the 'details' page in the GUI, or by running

.. code-block:: sh

   recipy annotate [run-id]


which will open an editor to allow you to write notes that will be attached to
the run. These will then be viewable via the command-line and the GUI when
searching for runs.

Saving Custom Values
====================

Command Line Interface
======================

There are other features in the command-line interface too: ``recipy --help``
to see the other options. You can view diffs, see all runs that created a file
with a given name, search based on ids, show the latest entry and more:

.. code-block:: sh

   recipy - a frictionless provenance tool for Python

   Usage:
     recipy search [options] <outputfile>
     recipy latest [options]
     recipy gui [options]
     recipy annotate [<idvalue>]
     recipy (-h | --help)
     recipy --version

   Options:
     -h --help     Show this screen
     --version     Show version
     -a --all      Show all results (otherwise just latest result given)
     -f --fuzzy    Use fuzzy searching on filename
     -r --regex    Use regex searching on filename
     -i --id       Search based on (a fragment of) the run ID
     -v --verbose  Be verbose
     -d --diff     Show diff
     -j --json     Show output as JSON
     --no-browser  Do not open browser window
     --debug       Turn on debugging mode


Configuration
=============

By default, recipy stores all of its configuration and the database itself in
``~/.recipy``. Recipy's  main configuration file is inside this folder, called
``recipyrc``. The configuration file format is very simple, and is based on
Windows INI files - and having a configuration file is completely optional:
the defaults will work fine with no configuration file.

An example configuration is:

.. code-block:: sh

   [ignored metadata]
   diff

   [general]
   debug


This simply instructs recipy not to save ``git diff`` information when it
records metadata about a run, and also to print debug messages (which can be
really useful if you're trying to work out why certain functions aren't
patched). At the moment, the only possible options are:

* ``[general]``

  * ``debug`` - print debug messages
  * ``editor = vi`` - Configure the default text editor that will be used when
  recipy needs you to type in a message. Use notepad if on Windows, for example
  * ``quiet`` - don't print any messages
  * ``port`` - specify port to use for the GUI

* ``[data]``

  * ``file_diff_outputs`` - store diff between the old output and new output
  file, if the output file exists before the script is executed

* ``[database]``

  * ``path = /path/to/file.json`` - set the path to the database file

* ``[ignored metadata]``

  * ``diff`` - don't store the output of ``git diff`` in the metadata for a
  recipy run
  * ``git`` - don't store anything relating to git (origin, commit, repo etc)
  in the metadata for a recipy run
  * ``input_hashes`` - don't compute and store SHA-1 hashes of input files
  * ``output_hashes`` - don't compute and store SHA-1 hashes of output files

* ``[ignored inputs]``

  * List any module here (eg. ``numpy``\ ) to instruct recipy *not* to record
  inputs from this module, or ``all`` to ignore inputs from all modules

* ``[ignored outputs]``

  * List any module here (eg. ``numpy``\ ) to instruct recipy *not* to record
  outputs from this module, or ``all`` to ignore outputs from all modules

By default all metadata is stored (ie. no metadata is ignored) and debug messages
are not shown. A ``.recipyrc`` file in the current directory takes precedence over
the ``~/.recipy/recipyrc`` file, allowing per-project configurations to be easily
handled.

**Note:** No default configuration file is provided with recipy, so if you wish
to configure anything you will need to create a properly-formatted file yourself.
