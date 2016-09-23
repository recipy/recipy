"""
Tests of 'diff' logging when recipy is used within Git.
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


class TestGit:
    """
    Tests of 'diff' logging when recipy is used within Git.
    """

    SCRIPT_NAME = "run_numpy.py"
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
        TestGit.directory = tempfile.mkdtemp(TestGit.__name__)
        TestGit.script = os.path.join(os.path.dirname(__file__),
                                      TestGit.SCRIPT_NAME)
        TestGit.original_script = TestGit.script + ".orig"
        shutil.copy(TestGit.script, TestGit.original_script)

    def teardown_method(self, method):
        """
        py.test teardown function, deletes test directory in $TEMP,
        and moves 'original_script' to 'script'.
        """
        if os.path.isdir(TestGit.directory):
            shutil.rmtree(TestGit.directory)
        os.remove(TestGit.script)
        os.rename(TestGit.original_script, TestGit.script)

    def test_git(self):
        """
        Running a script and then running it after it has been
        modified (via addition of a 'pass') no-op command should give
        the same results in the log (aside from their 'unique_id',
        'diff', 'date', 'exit_date', 'command_args', 'inputs' and
        'outputs'), and the 'diff' should record the change made to
        the file.
        """
        input_file = os.path.join(TestGit.directory, "input.csv")
        with open(input_file, "w") as csv_file:
            csv_file.write("1,4,9,16\n")
        output_file = os.path.join(TestGit.directory, "output.csv")

        # Run script.
        exit_code, _ = process.execute_and_capture(
            environment.get_python_exe(),
            [TestGit.script, input_file, output_file])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert log["diff"] == "", "Expected 'diff' to be empty"

        # Add "pass" as final line in script.
        with open(TestGit.original_script, "r") as source_file:
            lines = source_file.readlines()
        with open(TestGit.script, "w") as destination_file:
            destination_file.writelines(lines)
            destination_file.write("pass\n")

        # Re-run script.
        exit_code, _ = process.execute_and_capture(
            environment.get_python_exe(),
            [TestGit.script, input_file, output_file])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        git_log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert git_log["diff"] != "", "Expected 'diff' to be non-empty"

        # Search for diff-related mark-up.
        regexps = [
            r"---.*" + TestGit.SCRIPT_NAME + "\n",
            r"\+\+\+.*" + TestGit.SCRIPT_NAME + "\n",
            r"@@.*\n",
            r"\+pass.*\n"]
        helpers.search_regexps(git_log["diff"], regexps)
        # Important: assumes script inputs and outputs one or more files.
        # Check that input and output files recorded have the same
        # local names.
        for key in ["inputs", "outputs"]:
            assert len(log[key]) == len(git_log[key]),\
                   ("Expected same number of " + key + " files")
            [import_file, _] = log[key][0]
            [file, _] = git_log[key][0]
            assert os.path.basename(import_file) ==\
                os.path.basename(file),\
                "Expected local file names to be equal"
        # Remove fields that are specific to a run.
        for key in ["unique_id", "diff", "date", "exit_date",
                    "command_args", "inputs", "outputs"]:
            del log[key]
            del git_log[key]
        assert log == git_log,\
            ("Expected " + str(log) + " to equal " + str(git_log))
