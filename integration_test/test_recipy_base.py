"""
Base class for recipy tests.

Sub-classes use a Python script (run_numpy.py) about which the following
assumptions are made:

* Co-located with this test script, in the same directory.
* Imports recipy.
* Expects two arguments via the command-line: an input file
  name and an output file name.
* Reads the input file and creates the output file using a library
  which recipy is configured to log.
"""

# Copyright (c) 2016 University of Edinburgh.

import os
import os.path
import shutil
import tempfile
import git

from integration_test import environment
from integration_test import helpers
from integration_test import process


class TestRecipyBase(object):
    """
    Base class for recipy tests.
    """

    SCRIPT_NAME = "run_numpy.py"
    """ Test script assumed to be in same directory as this class. """

    def setup_method(self, method):
        """
        py.test setup function, creates test directory in $TEMP,
        initialises it as a Git repository, copies SCRIPT_NAME to it,
        creates input file, and commits SCRIPT_NAME.

        Note: this function defines member variables self.directory,
        self.script, self.original_script, self.input_file and
        self.output_file. These cannot be defined in an __init__
        constructor as py.test cannot collect test classes with
        constructors.

        :param method: Test method
        :type method: function
        """
        # Absolute path to temporary directory for these tests.
        self.directory = tempfile.mkdtemp(TestRecipyBase.__name__)
        # Absolute path to original copy of test script.
        self.original_script =\
            os.path.join(os.path.dirname(__file__),
                         TestRecipyBase.SCRIPT_NAME)
        # Absolute path to test script.
        self.script = os.path.join(self.directory,
                                   TestRecipyBase.SCRIPT_NAME)
        shutil.copy(self.original_script, self.script)
        # Absolute path to sample input data file for above script.
        self.input_file = os.path.join(self.directory, "input.csv")
        with open(self.input_file, "w") as csv_file:
            csv_file.write("1,4,9,16\n")
            csv_file.write("1,8,27,64\n")
            csv_file.write("\n")
        # Absolute path to sample output data file for above script.
        self.output_file = os.path.join(self.directory, "output.csv")
        repository = git.Repo.init(self.directory)
        repository.index.add([TestRecipyBase.SCRIPT_NAME])
        repository.index.commit("Initial commit")
        # Clear cache,
        # See: https://github.com/gitpython-developers/GitPython/issues/508
        repository.git.clear_cache()
        # Purge recipy ready for testing.
        helpers.clean_recipy()

    def teardown_method(self, method):
        """
        py.test teardown function, deletes test directory.

        :param method: Test method
        :type method: function
        """
        if os.path.isdir(self.directory):
            shutil.rmtree(self.directory)

    def run_script(self):
        """
        Run test_script using current Python executable.

        :return: (exit code, standard output and error)
        :rtype: (int, str or unicode)
        """
        return process.execute_and_capture(
            environment.get_python_exe(),
            [self.script, self.input_file, self.output_file])
