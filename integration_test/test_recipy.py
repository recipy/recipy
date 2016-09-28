"""
Tests of recipy commands.
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


class TestRecipy:
    """
    Tests of recipy commands.
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
            [TestRecipy.script,
             TestRecipy.input_file,
             TestRecipy.output_file])

    @classmethod
    def setup_class(cls):
        """
        py.test setup function, creates test directory in $TEMP,
        test_input_file path, test_input_file with CSV,
        test_output_file path.
        """
        TestRecipy.script =\
            os.path.join(os.path.dirname(__file__),
                         TestRecipy.SCRIPT_NAME)
        TestRecipy.directory =\
            tempfile.mkdtemp(TestRecipy.__name__)
        TestRecipy.input_file =\
            os.path.join(TestRecipy.directory, "input.csv")
        with open(TestRecipy.input_file, "w") as csv_file:
            csv_file.write("1,4,9,16\n")
            csv_file.write("1,8,27,64\n")
            csv_file.write("\n")
        TestRecipy.output_file =\
            os.path.join(TestRecipy.directory, "output.csv")
        TestRecipy.patterns = {}
        TestRecipy.patterns["-f"] = "input.c"
        TestRecipy.patterns["--fuzzy"] = "output.c"
        TestRecipy.patterns["-r"] = ".*inp.*"
        TestRecipy.patterns["--regex"] = ".*out.*"
        TestRecipy.patterns["-p"] = TestRecipy.input_file
        TestRecipy.patterns["--filepath"] = TestRecipy.output_file

    @classmethod
    def teardown_class(cls):
        """
        py.test teardown function, deletes test directory in $TEMP.
        """
        if os.path.isdir(TestRecipy.directory):
            shutil.rmtree(TestRecipy.directory)

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
        if os.path.isfile(TestRecipy.output_file):
            os.remove(TestRecipy.output_file)

    def compare_json_logs(self, log1, log2):
        """
        Compare two recipy JSON logs for equality.

        :param log1: Log
        :type log1: dict
        :param log2: Another log
        :type log2: dict
        :raises AssertionError: if log1 and log2 differ in their keys
        and/or values
        """
        # Convert dates from str or unicode to datetime.datetime.
        for key in ["date", "exit_date"]:
            log1[key] = environment.get_tinydatestr_as_date(log1[key])
            log2[key] = environment.get_tinydatestr_as_date(log2[key])
        assert log1 == log2, "Expected equal logs"

    def get_search(self, flag, run_id=None):
        """
        Get valid search flags and arguments for searches expected to
        succeed.

        :param flag: Search flag, or 'default' for file hash-based
        searches
        :type flag: str or unicode
        :param run_id: Run ID, used if flag is '-i' or '--id'
        :type run_id: str or unicode
        :return: flags and arguments
        :rtype: list of str or unicode
        """
        if flag in ["-i", "--id"]:
            return [flag, run_id]
        elif flag in TestRecipy.patterns.keys():
            return [flag, TestRecipy.patterns[flag]]
        else:
            return [TestRecipy.input_file]

    def get_unknown_search(self, flag):
        """
        Get search flags and arguments for searches expected to fail.

        :param flag: Search flag, or 'default' for file hash-based
        searches
        :type flag: str or unicode
        :return: flags and arguments
        :rtype: list of str or unicode
        """
        if flag != "default":
            return [flag, "unknown"]
        else:
            return ["unknown"]

    def test_no_arguments(self):
        """
        Test "recipy".
        """
        exit_code, stdout = process.execute_and_capture("recipy", [])
        assert exit_code == 1, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        helpers.search_regexps(stdout[0], ["Usage:\n"])

    def test_version(self):
        """
        Test "recipy --version".
        """
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["--version"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        helpers.search_regexps(stdout[0], [r"recipy v[0-9]\.[0-9]\.[0-9]"])

    @pytest.mark.parametrize("help_flag", ["-h", "--help"])
    def test_help(self, help_flag):
        """
        Test "recipy -h|--help".
        """
        exit_code, stdout = process.execute_and_capture("recipy", [help_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        regexps = [r"recipy - a frictionless provenance tool for Python\n",
                   r"Usage:\n",
                   r"Options:\n"]
        helpers.search_regexps(" ".join(stdout), regexps)

    def test_debug(self):
        """
        Test "recipy latest --debug", to look for debug-related output
        on stdout.
        """
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--debug"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        regexps = [r"Command-line arguments: \n",
                   r"DB path: .*\n",
                   r"Full config file \(as interpreted\):\n",
                   r"----------------------------------\n",
                   r"----------------------------------\n"]
        helpers.search_regexps(" ".join(stdout), regexps)

    def test_latest_empty_db(self):
        """
        Test "recipy latest" if no database.
        """
        exit_code, stdout = process.execute_and_capture("recipy", ["latest"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        assert 'Database is empty' in stdout[0]

    def test_latest(self):
        """
        Test "recipy latest".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        regexps = [r"Run ID: .*\n",
                   r"Created by .* on .*\n",
                   r"Ran .* using .*\n",
                   r"Git: commit .*, in .*, with origin .*\n",
                   r"Environment: .*\n",
                   r"Libraries: .*\n",
                   r"Inputs:\n",
                   r"Outputs:\n"]
        helpers.search_regexps(" ".join(stdout), regexps)

    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_latest_json(self, json_flag):
        """
        Test "recipy latest -j|--json".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        self.compare_json_logs(json_log, db_log)

    @pytest.mark.parametrize("search_flag", ["default",
                                             "-i", "--id",
                                             "-f", "--fuzzy",
                                             "-r", "--regex",
                                             "-p", "--filepath"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search(self, search_flag, json_flag):
        """
        Test "recipy search [-p|--filepath|-f|--fuzzy
        |-r|--regex] VALUE -j|--json".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        pattern = self.get_search(search_flag, unique_id)
        args = ["search"]
        args.extend(pattern)
        args.append(json_flag)
        exit_code, stdout = process.execute_and_capture("recipy", args)
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        # Handle case where 'recipy search HASH' returns a list
        if isinstance(json_log, list):
            json_log = json_log[0]
        self.compare_json_logs(json_log, db_log)

    @pytest.mark.parametrize("search_flag", ["default",
                                             "-i", "--id",
                                             "-f", "--fuzzy",
                                             "-r", "--regex",
                                             "-p", "--filepath"])
    def test_search_unknown(self, search_flag):
        """
        Test "recipy search [-i|--id|-p|--filepath|-f|--fuzzy
        |-r|--regex] UNKNOWN_VALUE".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        pattern = self.get_unknown_search(search_flag)
        args = ["search"]
        args.extend(pattern)
        exit_code, stdout = process.execute_and_capture("recipy", args)
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        assert 'No results found' in stdout[0]

    @pytest.mark.parametrize("search_flag", ["default",
                                             "-i", "--id",
                                             "-f", "--fuzzy",
                                             "-r", "--regex",
                                             "-p", "--filepath"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_unknown_json(self, search_flag, json_flag):
        """
        Test "recipy search [-i|--id|-p|--filepath|-f|--fuzzy
        |-r|--regex] UNKNOWN_VALUE -j|--json".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        pattern = self.get_unknown_search(search_flag)
        args = ["search"]
        args.extend(pattern)
        args.append(json_flag)
        exit_code, stdout = process.execute_and_capture("recipy", args)
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_logs = json.loads(" ".join(stdout))
        assert json_logs == [], "Expected []"

    @pytest.mark.parametrize("search_flag", ["default",
                                             "-f", "--fuzzy",
                                             "-r", "--regex",
                                             "-p", "--filepath"])
    @pytest.mark.parametrize("all_flag", ["-a", "--all"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_all(self, search_flag, all_flag, json_flag):
        """
        Test "recipy search [-p|--filepath|-f|--fuzzy
        |-r|--regex] VALUE -a|--all -j|--json".
        """
        num_runs = 3
        for i in range(num_runs):
            exit_code, _ = TestRecipy.run_script()
            assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        pattern = self.get_search(search_flag, unique_id)
        args = ["search"]
        args.extend(pattern)
        args.append(all_flag)
        args.append(json_flag)
        exit_code, stdout = process.execute_and_capture("recipy", args)
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_logs = json.loads(" ".join(stdout))
        assert num_runs == len(json_logs), "Unexpected number of JSON logs"

    @pytest.mark.parametrize("id_flag", ["-i", "--id"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_id_hash_prefix(self, id_flag, json_flag):
        """
        Test "recipy search -i|--id HASH_PREFIX [-j|--json]".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        half_id = unique_id[0:int(len(unique_id) / 2)]
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", id_flag, str(half_id), json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        assert len(json_log) == 1, "Expected a single JSON log"
        self.compare_json_logs(json_log[0], db_log)

    @pytest.mark.parametrize("search_flag", ["default",
                                             "-i", "--id",
                                             "-f", "--fuzzy",
                                             "-r", "--regex",
                                             "-p", "--filepath"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_bad_syntax(self, search_flag, json_flag):
        """
        Test "recipy search -p|--filepath|-f|--fuzzy
        |-r|--regex PATTERN VALUE -j|--json".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        pattern = self.get_search(search_flag, unique_id)
        args = ["search"]
        args.extend(pattern)
        args.append("value")
        args.append(json_flag)
        exit_code, stdout = process.execute_and_capture("recipy", args)
        assert exit_code == 1, ("Unexpected exit code " + str(exit_code))