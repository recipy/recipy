"""
Base class for recipy tests.
"""

# Copyright (c) 2016 University of Edinburgh.

import json
import os
import os.path
import shutil
import tempfile
import pytest

from integration_test import environment
from integration_test import helpers
from integration_test import process
from integration_test import recipy_environment as recipyenv


class TestRecipyBase(object):
    """
    Base class for recipy tests.
    """

    SCRIPT_NAME = "run_numpy.py"
    """ Test script assumed to be in same directory as this class. """
    script = ""
    """ Absolute path to test script. """
    directory = ""
    """ Absolute path to temporary directory for these tests. """
    input_file = ""
    """ Absolute path to sample input data file for above script. """
    output_file = ""
    """ Absolute path to sample output data file for above script. """
    patterns = {}
    """ Dictionary of search flags to patterns. """

    @classmethod
    def run_script(cls):
        """
        Run test_script using current Python executable.

        :return: (exit code, standard output and error)
        :rtype: (int, str or unicode)
        """
        return process.execute_and_capture(
            environment.get_python_exe(),
            [TestRecipyBase.script,
             TestRecipyBase.input_file,
             TestRecipyBase.output_file])

    @classmethod
    def setup_class(cls):
        """
        py.test setup function, creates test directory in $TEMP,
        test_input_file path, test_input_file with CSV,
        test_output_file path.
        """
        TestRecipyBase.script =\
            os.path.join(os.path.dirname(__file__),
                         TestRecipyBase.SCRIPT_NAME)
        TestRecipyBase.directory =\
            tempfile.mkdtemp(TestRecipyBase.__name__)
        TestRecipyBase.input_file =\
            os.path.join(TestRecipyBase.directory, "input.csv")
        with open(TestRecipyBase.input_file, "w") as csv_file:
            csv_file.write("1,4,9,16\n")
            csv_file.write("1,8,27,64\n")
            csv_file.write("\n")
        TestRecipyBase.output_file =\
            os.path.join(TestRecipyBase.directory, "output.csv")

    @classmethod
    def teardown_class(cls):
        """
        py.test teardown function, deletes test directory in $TEMP.
        """
        if os.path.isdir(TestRecipyBase.directory):
            shutil.rmtree(TestRecipyBase.directory)

    def setup_method(self, method):
        """
        py.test setup function, empties ~/.recipy, deletes recipyrc and
        .recipyrc.

        :param method: Test method
        :type method: function
        """
        helpers.clean_recipy()

    def teardown_method(self, method):
        """
        py.test teardown function, deletes output_file.

        :param method: Test method
        :type method: function
        """
        if os.path.isfile(TestRecipyBase.output_file):
            os.remove(TestRecipyBase.output_file)
