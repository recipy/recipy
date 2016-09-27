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
        TestRecipy.patterns["-f"] = "input.cs"
        TestRecipy.patterns["--fuzzy"] = "input.cs"
        TestRecipy.patterns["-r"] = ".*input.*"
        TestRecipy.patterns["--regex"] = ".*input.*"
        TestRecipy.patterns["-p"] = TestRecipy.input_file
        TestRecipy.patterns["--filepath"] = TestRecipy.input_file

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

    @pytest.mark.parametrize("regex_flag", ["-r", "--regex"])
    @pytest.mark.parametrize("pattern",
                             [".*input.csv", ".*inp.*",
                              ".*output.csv", ".*out.*"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_r(self, regex_flag, pattern, json_flag):
        """
        Test "recipy search -r|--regex PATTERN -j|--json".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", regex_flag, pattern, json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        self.compare_json_logs(json_log, db_log)

    @pytest.mark.parametrize("regex_flag", ["-r", "--regex"])
    def test_search_r_unknown(self, regex_flag):
        """
        Test "recipy search -r|--regex NO_MATCHING_PATTERN".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", regex_flag, ".*unknown.*"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        assert 'No results found' in stdout[0]

    @pytest.mark.parametrize("path_flag", ["-p", "--filepath"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_p(self, path_flag, json_flag):
        """
        Test "recipy search -p|--filepath FILE [-j|--json]".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        for f in [TestRecipy.input_file, TestRecipy.output_file]:
            exit_code, stdout = process.execute_and_capture(
                "recipy", ["search", path_flag, f, json_flag])
            assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
            assert len(stdout) > 0, "Expected stdout"
            json_log = json.loads(" ".join(stdout))
            db_log, _ = helpers.get_log(recipyenv.get_recipydb())
            self.compare_json_logs(json_log, db_log)

    @pytest.mark.parametrize("path_flag", ["-p", "--filepath"])
    def test_search_p_unknown(self, path_flag):
        """
        Test "recipy search -p|--filepath NO_MATCHING_FILE".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", path_flag, "unknown.csv"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        assert 'No results found' in stdout[0]

    def test_search_i_unknown(self, id):
        """
        Test "recipy search -i unknown" if no database.
        """
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", "-i", "unknown"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        assert 'No results found' in stdout[0]

    @pytest.mark.parametrize("id_flag", ["-i", "--id"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_i(self, id_flag, json_flag):
        """
        Test "recipy search -i|--id HASH [-j|--json]".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", id_flag, str(unique_id), json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        assert len(json_log) == 1, "Expected a single JSON log"
        self.compare_json_logs(json_log[0], db_log)

    @pytest.mark.parametrize("id_flag", ["-i", "--id"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_i(self, id_flag, json_flag):
        """
        Test "recipy search -i|--id HASH [-j|--json]".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", id_flag, str(unique_id), json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        assert len(json_log) == 1, "Expected a single JSON log"
        self.compare_json_logs(json_log[0], db_log)

    @pytest.mark.parametrize("id_flag", ["-i", "--id"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_i_hash_prefix(self, id_flag, json_flag):
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

    @pytest.mark.parametrize("id_flag", ["-i", "--id"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_i_unknown(self, id_flag, json_flag):
        """
        Test "recipy search -i|--id UNKNOWN_HASH -j|--json".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", id_flag, "unknown", json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        assert json_log == [], "Expected []"

    @pytest.mark.parametrize("fuzzy_flag", ["-f", "--fuzzy"])
    @pytest.mark.parametrize("pattern",
                             ["input.cs", "inp",
                              "output.cs", "out"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_f(self, fuzzy_flag, pattern, json_flag):
        """
        Test "recipy search -f|--fuzzy PATTERN -j|--json".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", fuzzy_flag, pattern, json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        self.compare_json_logs(json_log, db_log)

    @pytest.mark.parametrize("fuzzy_flag", ["-f", "--fuzzy"])
    def test_search_f_unknown(self, fuzzy_flag):
        """
        Test "recipy search -f|--fuzzy NO_MATCHING_PATTERN".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", fuzzy_flag, "unknown"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        assert 'No results found' in stdout[0]

    @pytest.mark.parametrize("flag", ["-i", "--id",
                                      "-p", "--filepath",
                                      "-f", "--fuzzy",
                                      "-r", "--regex"])
    def test_search_bad_syntax(self, flag):
        """
"        Test "recipy search -i|--id|-p|--filepath|-f|--fuzzy
        |-r|--regex VALUE UNEXPECTED_VALUE".
        """
        exit_code, _ = TestRecipy.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        half_id = unique_id[0:int(len(unique_id) / 2)]
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", flag, "value", "unexpected_value"])
        assert exit_code == 1, ("Unexpected exit code " + str(exit_code))

    @pytest.mark.parametrize("search_flag", ["-f", "--fuzzy",
                                             "-r", "--regex",
                                             "-p", "--filepath"])
    @pytest.mark.parametrize("all_flag", ["-a", "--all"])
    def test_search_all(self, search_flag, all_flag):
        """
        Test "recipy search -i|--id|-p|--filepath|-f|--fuzzy
        |-r|--regex VALUE -j -a|--all".
        """
        num_runs = 3
        for i in range(num_runs):
            exit_code, _ = TestRecipy.run_script()
            assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        pattern = TestRecipy.patterns[search_flag]
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", search_flag, pattern, "-j", all_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
#        print(stdout)
        json_logs = json.loads(" ".join(stdout))
        assert num_runs == len(json_logs), "Unexpected number of JSON logs"
