"""
Tests of recipy configuration, provided via recipyrc configuration
files.
"""

# Copyright (c) 2016 University of Edinburgh.

import os
import os.path
import shutil
import tempfile
import pytest

from integration_test import environment
from integration_test import helpers
from integration_test import process
from integration_test import recipy_environment as recipyenv


class TestRecipyrc:
    """
    Tests of recipy configuration, provided via recipyr configuration
    files.
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

    @classmethod
    def run_script(cls):
        """
        Run test_script using current Python executable.

        :return: (exit code, standard output and error)
        :rtype: (int, str or unicode)
        """
        return process.execute_and_capture(
            environment.get_python_exe(),
            [TestRecipyrc.script,
             TestRecipyrc.input_file,
             TestRecipyrc.output_file])

    @classmethod
    def setup_class(cls):
        """
        py.test setup function, creates test directory in $TEMP,
        test_input_file path, test_input_file with CSV,
        test_output_file path.
        """
        TestRecipyrc.script =\
            os.path.join(os.path.dirname(__file__),
                         TestRecipyrc.SCRIPT_NAME)
        TestRecipyrc.directory =\
            tempfile.mkdtemp(TestRecipyrc.__name__)
        TestRecipyrc.input_file =\
            os.path.join(TestRecipyrc.directory, "input.csv")
        with open(TestRecipyrc.input_file, "w") as csv_file:
            csv_file.write("1,4,9,16\n")
            csv_file.write("1,8,27,64\n")
            csv_file.write("\n")
        TestRecipyrc.output_file =\
            os.path.join(TestRecipyrc.directory, "output.csv")

    @classmethod
    def teardown_class(cls):
        """
        py.test teardown function, deletes test directory in $TEMP.
        """
        if os.path.isdir(TestRecipyrc.directory):
            shutil.rmtree(TestRecipyrc.directory)

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
        if os.path.isfile(TestRecipyrc.output_file):
            os.remove(TestRecipyrc.output_file)

    def test_recipyrc(self):
        """
        If neither .recipyrc, recipyrc nor ~/recipyrc exist then
        recipy should use its default configuration. A check is also
        done to see that the database is created in
        ~/recipy/recipyDB.json.
        """
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        recipydb = recipyenv.get_recipydb()
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    @pytest.mark.parametrize("recipyrc", [
        recipyenv.get_recipyrc(),
        recipyenv.get_local_recipyrc(),
        recipyenv.get_local_dotrecipyrc()])
    def test_user_recipyrc(self, recipyrc):
        """
        If one of ~/recipy/recipyrc, .recipy or recipyrc are present
        then their configuration is used. A check is also done to see
        that if [database].path is valid then the database is created
        at that path.

        :param recipyrc: recipyrc file
        :type recipyrc: str or unicode
        """
        recipydb = os.path.join(TestRecipyrc.directory,
                                str(id(self)) + "DB.json")
        helpers.update_recipyrc(recipyrc, "database", "path", recipydb)
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    @pytest.mark.parametrize("recipyrc_files", [
        (recipyenv.get_local_dotrecipyrc(), recipyenv.get_recipyrc()),
        (recipyenv.get_local_recipyrc(), recipyenv.get_recipyrc()),
        (recipyenv.get_local_recipyrc(), recipyenv.get_local_dotrecipyrc())])
    def test_recipyrc_precedence(self, recipyrc_files):
        """
        Check recipyrc precedence if multiple recipyrc files exist.

        * .recipyrc is used in preference to ~/recipy/recipyrc.
        * recipyrc is used in preference to ~/recipy/recipyrc.
        * recipyrc is used in preference to .recipyrc.

        :param recipyrc_files: (recipyrc file, recipyrc file), the
        former is expected to take precedence
        :type recipyrc_files: (str or unicode, str or unicode)
        """
        (recipyrc, ignore_recipyrc) = recipyrc_files
        recipydb = os.path.join(TestRecipyrc.directory,
                                str(id(self)) + "DB.json")
        helpers.update_recipyrc(recipyrc,
                                "database", "path", recipydb)
        ignore_recipydb = os.path.join(TestRecipyrc.directory,
                                       str(id(self)) + "ignoreDB.json")
        helpers.update_recipyrc(ignore_recipyrc,
                                "database", "path", ignore_recipydb)
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)
        assert not os.path.isfile(ignore_recipydb),\
            ("Did not expect to find " + ignore_recipydb)

    def test_unknown_section(self):
        """
        If recipyrc has an unknown section then the section is ignored
        and does not prevent recipy from running.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc,
                                "unknown", "unknown", "unknown")
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        recipydb = recipyenv.get_recipydb()
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    def test_unknown_parameter(self):
        """
        If recipyrc has a section with an unknown key then the key is
        ignored and does not prevent recipy from running.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc,
                                "database", "unknown", "unknown")
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        recipydb = recipyenv.get_recipydb()
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    def test_unknown_database_path(self):
        """
        If [database].path has an invalid directory then recipy fails
        with exit code 1.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "database", "path", "unknown")
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 1, ("Unexpected exit code " + str(exit_code))

    def test_general_debug(self):
        """
        If [general].debug is present then debugging information is
        printed.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "general", "debug")
        exit_code, stdout = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        # Important: order of log statements is tightly-coupled to
        # script.
        debugs = ["recipy run inserted",
                  "Patching",
                  "Patching input function",
                  "Patching output function",
                  "Input from",
                  "Output to",
                  "recipy run complete"]
        for line in stdout:
            debug = debugs[0]
            if debug in line:
                debugs.remove(debug)
        assert len(debugs) == 0, ("Expected debug statements " +
                                  str(debugs))

    def test_general_quiet(self):
        """
        If [general].quiet is present then no recipy information is
        printed.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "general", "quiet")
        exit_code, stdout = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        # Important: assumes script does no output of its own.
        assert len(stdout) == 0, ("Unexpected output " + str(stdout))

    @pytest.mark.parametrize("ignores", [
        ("input_hashes", "inputs"),
        ("output_hashes", "outputs")])
    def test_ignored_metadata_hashes(self, ignores):
        """
        If [ignored metadata].input_hases or output_hashes are present
        then no hashes are recorded for input/output files.

        :param ignores: (recipyrc configuration key, recipy log key),
        if the former is in [ignored metadata] the latter should not
        be in the log
        :type ignores: (str or unicode, str or unicode)
        """
        (recipyrc_key, log_key) = ignores
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "ignored metadata",
                                recipyrc_key)
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        # Important: assumes script inputs and outputs one or more files.
        (log, _) = helpers.get_log(recipyenv.get_recipydb())
        files = log[log_key]
        assert len(files) >= 1, "Unexpected number of files"
        assert not isinstance(files[0], list), "Unexpected list"

    def test_data_file_diff_outputs(self):
        """
        If [data].file_diff_outputs is present then:

        * If output files are created, then there are no 'filediffs'
              for the run.
        * If output files with the same content are created, then
             there are 'filediffs' for the run, with an empty 'diffs'
          value.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "data", "file_diff_outputs")
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        _, filediffs = helpers.get_log(recipyenv.get_recipydb())
        assert filediffs is None, "Expected filediffs to be None"

        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        _, filediffs = helpers.get_log(recipyenv.get_recipydb())
        assert filediffs is not None, "Expected filediffs not to be None"
        assert filediffs["filename"] == TestRecipyrc.output_file,\
            ("Expected filediffs['filename'] to be " +
             TestRecipyrc.output_file)
        assert filediffs["diff"] == ""

    def test_data_file_diff_outputs_diff(self):
        """
        If [data].file_diff_outputs is present, if output files
        are changed, then there will be 'filediffs' for that run, with
        a 'diffs' value describing changes to the output files.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "data", "file_diff_outputs")
        # Create an empty output file.
        open(TestRecipyrc.output_file, 'w').close()
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        _, filediffs = helpers.get_log(recipyenv.get_recipydb())
        assert filediffs is not None, "Expected filediffs not to be None"
        assert filediffs["filename"] == TestRecipyrc.output_file,\
            ("Expected filediffs['filename'] to be " +
             TestRecipyrc.output_file)
        assert "before this run" in filediffs["diff"],\
               "Expected 'before this run' in filediffs['diffs']"
        assert "after this run" in filediffs["diff"],\
               "Expected 'after this run' in filediffs['diffs']"

    @pytest.mark.parametrize("ignores", [
        ("ignored inputs", "inputs"),
        ("ignored outputs", "outputs")])
    def test_ignored_inputs_outputs(self, ignores):
        """
        If [ignored inputs] or [ignored outputs] entries are present,
        with a package name, then no 'inputs' or 'outputs' are present
        in logs when the package is used.

        :param ignores: (recipyrc configuration key, recipy log key),
        if a package is in the former, then the latter should not
        record files input/output by that package.
        :type ignores: (str or unicode, str or unicode)
        """
        (recipyrc_key, log_key) = ignores
        recipyrc = recipyenv.get_recipyrc()
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert len(log[log_key]) > 0, "Expected functions to be logged"

        # Important: assumes script uses "numpy".
        helpers.update_recipyrc(recipyrc, recipyrc_key, "numpy")
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert len(log[log_key]) == 0, "Expected no functions to be logged"

    @pytest.mark.parametrize("ignores", [
        ("ignored inputs", "inputs"),
        ("ignored outputs", "outputs")])
    def test_ignored_inputs_outputs_all(self, ignores):
        """
        If [ignored inputs] or [ignored outputs] entries are present,
        with "all", then no 'inputs' or 'outputs' are present
        in logs.

        :param ignores: (recipyrc configuration key, recipy log key),
        if "all" is in the former, then the latter should not
        record files input/output.
        :type ignores: (str or unicode, str or unicode)
        """
        (recipyrc_key, log_key) = ignores
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, recipyrc_key, "all")
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert len(log[log_key]) == 0, "Expected no functions to be logged"

    def test_ignored_metadata_diff(self):
        """
        If [ignored metadata].diff is present then no 'diff'
        information is in the log.
        """
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert "diff" in log, "Expected 'diff' in log"
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "ignored metadata", "diff")
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert "diff" not in log, "Unexpected 'diff' in log"

    def test_ignored_metadata_git(self):
        """
        If [ignored metadata].git is present then no 'gitrepo',
        'gitorigin', 'gitcommit' information is in the log.
        """
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        keys = ["gitrepo", "gitorigin", "gitcommit"]
        for key in keys:
            assert key in log, ("Expected " + key + " in log")
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "ignored metadata", "git")
        exit_code, _ = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        for key in keys:
            assert key not in log, ("Unexpected " + key + " in log")
