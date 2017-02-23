"""
Tests of recipy configuration, provided via recipyrc configuration
files.
"""

# Copyright (c) 2016 University of Edinburgh.

import os
import os.path
import pytest

from integration_test import helpers
from integration_test import recipy_environment as recipyenv
from integration_test import regexps
from integration_test import test_recipy_base


class TestRecipyrc(test_recipy_base.TestRecipyBase):
    """
    Tests of recipy configuration, provided via recipyr configuration
    files.
    """

    def test_recipyrc(self):
        """
        If neither .recipyrc, recipyrc nor ~/recipyrc exist then
        recipy should use its default configuration. A check is also
        done to see that the database is created in
        ~/recipy/recipyDB.json.
        """
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
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
        recipydb = os.path.join(self.directory,
                                str(id(self)) + "DB.json")
        helpers.update_recipyrc(recipyrc, "database", "path", recipydb)
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
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
        recipydb = os.path.join(self.directory,
                                str(id(self)) + "DB.json")
        helpers.update_recipyrc(recipyrc, "database", "path", recipydb)
        ignore_recipydb = os.path.join(self.directory,
                                       str(id(self)) + "ignoreDB.json")
        helpers.update_recipyrc(ignore_recipyrc, "database", "path",
                                ignore_recipydb)
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)
        assert not os.path.isfile(ignore_recipydb),\
            ("Did not expect to find " + ignore_recipydb)

    def test_unknown_section(self):
        """
        If recipyrc has an unknown section then the section is ignored
        and does not prevent recipy from running.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "unknown", "unknown",
                                "unknown")
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        recipydb = recipyenv.get_recipydb()
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    def test_unknown_parameter(self):
        """
        If recipyrc has a section with an unknown key then the key is
        ignored and does not prevent recipy from running.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "database", "unknown",
                                "unknown")
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        recipydb = recipyenv.get_recipydb()
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    def test_unknown_database_path(self):
        """
        If [database].path has an invalid directory then recipy fails
        with exit code 1.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "database", "path", "unknown")
        helpers.execute_python([self.script, self.input_file,
                                self.output_file], 1)

    def test_general_debug(self):
        """
        If [general].debug is present then debugging information is
        printed.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "general", "debug")
        _, stdout = helpers.execute_python([self.script,
                                            self.input_file,
                                            self.output_file])
        # Order of log statements from get_debug_regexps
        # is tightly-coupled to script.
        helpers.assert_matches_regexps(" ".join(stdout),
                                       regexps.get_debug())

    def test_general_quiet(self):
        """
        If [general].quiet is present then no recipy information is
        printed.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "general", "quiet")
        _, stdout = helpers.execute_python([self.script,
                                            self.input_file,
                                            self.output_file])
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
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        log, _ = helpers.get_log(recipyenv.get_recipydb())
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
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        _, filediffs = helpers.get_log(recipyenv.get_recipydb())
        assert filediffs is None, "Expected filediffs to be None"

        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        _, filediffs = helpers.get_log(recipyenv.get_recipydb())
        assert filediffs is not None, "Expected filediffs not to be None"
        assert filediffs["filename"] == self.output_file,\
            ("Expected filediffs['filename'] to be " + self.output_file)
        assert filediffs["diff"] == "",\
            "Expected filediffs['diff'] to be empty"

    def test_data_file_diff_outputs_diff(self):
        """
        If [data].file_diff_outputs is present, if output files
        are changed, then there will be 'filediffs' for that run, with
        a 'diff' value describing changes to the output files.
        """
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "data", "file_diff_outputs")
        # Create empty output file.
        open(self.output_file, 'w').close()
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        _, filediffs = helpers.get_log(recipyenv.get_recipydb())
        assert filediffs is not None, "Expected filediffs not to be None"
        assert filediffs["filename"] == self.output_file,\
            ("Expected filediffs['filename'] to be " + self.output_file)
        helpers.assert_matches_regexps(filediffs['diff'],
                                       regexps.get_filediffs())

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
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert len(log[log_key]) > 0, "Expected functions to be logged"

        helpers.update_recipyrc(recipyrc, recipyrc_key,
                                TestRecipyrc.LIBRARY)
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
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
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert len(log[log_key]) == 0, "Expected no functions to be logged"

    def test_ignored_metadata_diff(self):
        """
        If [ignored metadata].diff is present then no 'diff'
        information is in the log.
        """
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert "diff" in log, "Expected 'diff' in log"
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "ignored metadata", "diff")
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        assert "diff" not in log, "Unexpected 'diff' in log"

    def test_ignored_metadata_git(self):
        """
        If [ignored metadata].git is present then no 'gitrepo',
        'gitorigin', 'gitcommit' information is in the log.
        """
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        keys = ["gitrepo", "gitorigin", "gitcommit"]
        for key in keys:
            assert key in log, ("Expected " + key + " in log")
        recipyrc = recipyenv.get_recipyrc()
        helpers.update_recipyrc(recipyrc, "ignored metadata", "git")
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        for key in keys:
            assert key not in log, ("Unexpected " + key + " in log")
