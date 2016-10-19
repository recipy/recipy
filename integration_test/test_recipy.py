"""
Tests of recipy commands.
"""

# Copyright (c) 2016 University of Edinburgh.

import os
import json
import pytest

from integration_test import helpers
from integration_test import process
from integration_test import recipy_environment as recipyenv
from integration_test import regexps
from integration_test import test_recipy_base


class TestRecipy(test_recipy_base.TestRecipyBase):
    """
    Tests of recipy commands.
    """

    def setup_method(self, method):
        """
        py.test setup function, initialises dictionary of search flags to
        search patterns.
        Note: this function defines member variable self.patterns. This
        cannot be defined in an __init__ constructor as py.test cannot
        collect test classes with constructors.

        :param method: Test method
        :type method: function
        """
        super(TestRecipy, self).setup_method(method)
        input_base = os.path.basename(self.input_file)
        output_base = os.path.basename(self.output_file)
        # Dictionary of search flags to patterns.
        self.patterns = {}
        self.patterns["-f"] = input_base[0:len(input_base) - 2]
        self.patterns["--fuzzy"] = output_base[0:len(output_base) - 2]
        self.patterns["-r"] = ".*" + input_base[0:4] + ".*"
        self.patterns["--regex"] = ".*" + output_base[0:4] + ".*"
        self.patterns["-p"] = self.input_file
        self.patterns["--filepath"] = self.output_file
        # Run test script
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])

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
        elif flag in list(self.patterns.keys()):
            return [flag, self.patterns[flag]]
        else:
            return [self.input_file]

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

    def modify_script(self):
        """
        Add "pass" as final line in script.
        """
        with open(self.original_script, "r") as source_file:
            lines = source_file.readlines()
        with open(self.script, "w") as destination_file:
            destination_file.writelines(lines)
            destination_file.write("pass\n")

    def test_no_arguments(self):
        """
        Test "recipy".
        """
        exit_code, stdout = process.execute_and_capture("recipy", [])
        assert exit_code == 1, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        helpers.assert_matches_regexps(" ".join(stdout),
                                       regexps.get_usage())

    def test_version(self):
        """
        Test "recipy --version".
        """
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["--version"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        helpers.assert_matches_regexps(" ".join(stdout),
                                       regexps.get_version())

    @pytest.mark.parametrize("help_flag", ["-h", "--help"])
    def test_help(self, help_flag):
        """
        Test "recipy -h|--help".
        """
        exit_code, stdout = process.execute_and_capture("recipy", [help_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        helpers.assert_matches_regexps(" ".join(stdout), regexps.get_help())

    def test_debug(self):
        """
        Test "recipy latest --debug", to look for debug-related output
        on stdout.
        """
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--debug"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        helpers.assert_matches_regexps(" ".join(stdout),
                                       regexps.get_debug_recipy())

    def test_latest_empty_db(self):
        """
        Test "recipy latest" if no database.
        """
        helpers.clean_recipy()
        exit_code, stdout = process.execute_and_capture("recipy", ["latest"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        helpers.assert_matches_regexps(" ".join(stdout),
                                       regexps.get_db_empty())

    def test_latest(self):
        """
        Test "recipy latest".
        """
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        # Validate using logged data
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        helpers.assert_matches_regexps(" ".join(stdout),
                                       regexps.get_stdout(db_log))

    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_latest_json(self, json_flag):
        """
        Test "recipy latest -j|--json".
        """
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        helpers.assert_equal_json_logs(json_log, db_log)

    def test_latest_diff(self):
        """
        Test "recipy latest --diff".
        """
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--diff"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        # Validate standard output.
        helpers.assert_matches_regexps(" ".join(stdout),
                                       regexps.get_stdout(db_log))
        # Validate logged data
        assert db_log["diff"] == "", "Expected 'diff' to be empty"

        self.modify_script()
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])

        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--diff"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        diff_db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        # Validate standard output.
        helpers.assert_matches_regexps(" ".join(stdout),
                                       regexps.get_stdout(diff_db_log))
        helpers.assert_matches_regexps(
            " ".join(stdout),
            regexps.get_diff(TestRecipy.SCRIPT_NAME))
        # Validate logged data
        assert diff_db_log["diff"] != "", "Expected 'diff' to be non-empty"
        helpers.assert_matches_regexps(
            diff_db_log["diff"],
            regexps.get_diff(TestRecipy.SCRIPT_NAME))

        # Compare original log to diff log.
        for key in ["inputs", "outputs"]:
            assert len(db_log[key]) == len(diff_db_log[key]),\
                   ("Expected same number of " + key + " files")
            for index in range(0, len(db_log[key])):
                [original_file, _] = db_log[key][index]
                [diff_file, _] = diff_db_log[key][index]
                assert os.path.basename(original_file) ==\
                    os.path.basename(diff_file),\
                    "Expected local file names to be equal"
        # Remove fields that are specific to a run.
        for key in ["unique_id", "diff", "date", "exit_date",
                    "command_args", "inputs", "outputs"]:
            del db_log[key]
            del diff_db_log[key]
        assert db_log == diff_db_log,\
            ("Expected " + str(db_log) + " to equal " + str(diff_db_log))

    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_latest_diff_json(self, json_flag):
        """
        Test "recipy latest --diff -j|--json".
        """
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--diff", json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        helpers.assert_equal_json_logs(json_log, db_log)
        assert json_log["diff"] == "", "Expected 'diff' to be empty"

        self.modify_script()
        helpers.execute_python([self.script, self.input_file,
                                self.output_file])

        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--diff", json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        helpers.assert_equal_json_logs(json_log, db_log)
        assert json_log["diff"] != "", "Expected 'diff' to be non-empty"
        helpers.assert_matches_regexps(
            json_log["diff"],
            regexps.get_diff(TestRecipy.SCRIPT_NAME))

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
        helpers.assert_equal_json_logs(json_log, db_log)

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
        pattern = self.get_unknown_search(search_flag)
        args = ["search"]
        args.extend(pattern)
        exit_code, stdout = process.execute_and_capture("recipy", args)
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        helpers.assert_matches_regexps(" ".join(stdout),
                                       regexps.get_no_results())

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
        for _ in range(num_runs):
            helpers.execute_python([self.script, self.input_file,
                                    self.output_file])
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
        assert num_runs + 1 == len(json_logs),\
            "Unexpected number of JSON logs"

    @pytest.mark.parametrize("id_flag", ["-i", "--id"])
    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_search_id_hash_prefix(self, id_flag, json_flag):
        """
        Test "recipy search -i|--id HASH_PREFIX [-j|--json]".
        """
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        half_id = unique_id[0:int(len(unique_id) / 2)]
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["search", id_flag, str(half_id), json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        assert len(json_log) == 1, "Expected a single JSON log"
        helpers.assert_equal_json_logs(json_log[0], db_log)

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
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        pattern = self.get_search(search_flag, unique_id)
        args = ["search"]
        args.extend(pattern)
        args.append("value")
        args.append(json_flag)
        exit_code, _ = process.execute_and_capture("recipy", args)
        assert exit_code == 1, ("Unexpected exit code " + str(exit_code))
