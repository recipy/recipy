"""
Tests of 'python -m recipy' usage.

This script uses a Python script (run_numpy_no_recipy.py) about
which the following assumptions are made:

* Co-located with this test script, in the same directory.
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

from integration_test import environment
from integration_test import helpers
from integration_test import process
from integration_test import recipy_environment as recipyenv


class TestMflag:
    """
    Tests of 'python -m recipy' usage.
    """

    SCRIPT_NAME = "run_numpy_no_recipy.py"
    """ Test script assumed to be in same directory as this class. """
    script = ""
    """ Absolute path to test script. """
    original_script = ""
    """ Absolute path to original copy of test script. """
    directory = ""
    """ Absolute path to temporary directory for these tests. """

    def setup_method(self, method):
        """
        py.test setup function, creates test directory in $TEMP,
        sets 'script' with path to SCRIPT_NAME and copies script from
        'script' to 'original_script'.

        :param method: Test method
        :type method: function
        """
        TestMflag.directory = tempfile.mkdtemp(TestMflag.__name__)
        TestMflag.script = os.path.join(os.path.dirname(__file__),
                                        TestMflag.SCRIPT_NAME)
        TestMflag.original_script = TestMflag.script + ".orig"
        shutil.copy(TestMflag.script, TestMflag.original_script)

    def teardown_method(self, method):
        """
        py.test teardown function, deletes test directory in $TEMP,
        and moves 'original_script' to 'script'.
        """
        if os.path.isdir(TestMflag.directory):
            shutil.rmtree(TestMflag.directory)
        os.remove(TestMflag.script)
        os.rename(TestMflag.original_script, TestMflag.script)

    def test_m_recipy(self):
        """
        Running 'python -m recipy script' and the same script that
        inclues 'import recipy' should give the same results in the
        log (aside from their 'unique_id', 'diff', 'date',
        'exit_date', 'command_args', 'inputs' and 'outputs').
        """
        input_file = os.path.join(TestMflag.directory, "input.csv")
        with open(input_file, "w") as csv_file:
            csv_file.write("1,4,9,16\n")
        output_file = os.path.join(TestMflag.directory, "output.csv")

        exit_code, _ = process.execute_and_capture(
            environment.get_python_exe(),
            ["-m", "recipy", TestMflag.script,
             input_file, output_file])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        module_log, _ = helpers.get_log(recipyenv.get_recipydb())

        helpers.enable_recipy(TestMflag.original_script, TestMflag.script)

        exit_code, _ = process.execute_and_capture(
            environment.get_python_exe(),
            [TestMflag.script, input_file, output_file])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        import_log, _ = helpers.get_log(recipyenv.get_recipydb())
        for key in ["inputs", "outputs"]:
            assert len(module_log[key]) == len(import_log[key]),\
                   ("Expected same number of " + key + " files")
            for index in range(0, len(module_log[key])):
                [import_file, _] = module_log[key][index]
                [module_file, _] = import_log[key][index]
                assert os.path.basename(import_file) ==\
                    os.path.basename(module_file),\
                    "Expected local file names to be equal"
        # Remove fields that are specific to a run.
        for key in ["unique_id", "diff", "date", "exit_date",
                    "command_args", "inputs", "outputs"]:
            if key in module_log:
                del module_log[key]
                del import_log[key]
        assert module_log == import_log,\
            ("Expected " + str(module_log) + " to equal " +
             str(import_log))
