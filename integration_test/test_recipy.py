"""
Tests of recipy commands.
"""

# Copyright (c) 2016 University of Edinburgh.

import json
import pytest

from integration_test import helpers
from integration_test import process
from integration_test import recipy_environment as recipyenv
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
        # Dictionary of search flags to patterns.
        self.patterns = {}
        self.patterns["-f"] = "input.c"
        self.patterns["--fuzzy"] = "output.c"
        self.patterns["-r"] = ".*inp.*"
        self.patterns["--regex"] = ".*out.*"
        self.patterns["-p"] = self.input_file
        self.patterns["--filepath"] = self.output_file

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

    def get_stdout_regexps(self, log):
        """
        Get regular expressions with expected "diff" information
        corresponding to modification of modify_script.

        :param log: Recipy database log
        :type log: dict
        :returns: regular expressions
        :rtype: list of str or unicode
        """
        regexps = [r"Run ID: " + log["unique_id"] + "\n",
                   r"Created by " + log["author"] + " on .*\n",
                   r"Ran " + log["script"].replace("\\", "\\\\") +
                   " using .*\n",
                   r"Git: commit " + log["gitcommit"] +
                   ", in repo " +
                   log["gitrepo"].replace("\\", "\\\\") +
                   ", with origin " + str(log["gitorigin"]) + ".*\n",
                   r"Environment: .*\n",
                   r"Libraries: " + ", ".join(log["libraries"]) + "\n",
                   r"Inputs:\n",
                   log["inputs"][0][0].replace("\\", "\\\\"),
                   log["inputs"][0][1],
                   log["inputs"][0][0].replace("\\", "\\\\") +
                   r" \(" + log["inputs"][0][1] + r"\)\n",
                   r"Outputs:\n",
                   log["outputs"][0][0].replace("\\", "\\\\") +
                   r" \(" + log["outputs"][0][1] + r"\)\n"]
        return regexps

    def test_latest(self):
        """
        Test "recipy latest".
        """
        exit_code, _ = self.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        # Validate using logged data
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        regexps = self.get_stdout_regexps(db_log)
        helpers.search_regexps(" ".join(stdout), regexps)

    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_latest_json(self, json_flag):
        """
        Test "recipy latest -j|--json".
        """
        exit_code, _ = self.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        helpers.compare_json_logs(json_log, db_log)

    def modify_script(self):
        """
        Add "pass" as final line in script.
        """
        with open(self.original_script, "r") as source_file:
            lines = source_file.readlines()
        with open(self.script, "w") as destination_file:
            destination_file.writelines(lines)
            destination_file.write("pass\n")

    def get_diff_regexps(self):
        """
        Get regular expressions with expected "diff" information
        corresponding to modification of modify_script.

        :returns: regular expressions
        :rtype: list of str or unicode
        """
        regexps = [
            r"---.*" + TestRecipy.SCRIPT_NAME + "\n",
            r"\+\+\+.*" + TestRecipy.SCRIPT_NAME + "\n",
            r"@@.*\n",
            r"\+pass.*\n"]
        return regexps

    def test_latest_diff(self):
        """
        Test "recipy latest --diff".
        """
        exit_code, _ = self.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--diff"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        # Validate using logged data
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        regexps = self.get_stdout_regexps(db_log)
        helpers.search_regexps(" ".join(stdout), regexps)

        self.modify_script()

        exit_code, _ = self.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--diff"])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        # Validate using logged data
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        regexps = self.get_stdout_regexps(db_log)
        regexps.extend(self.get_diff_regexps())
        helpers.search_regexps(" ".join(stdout), regexps)

    @pytest.mark.parametrize("json_flag", ["-j", "--json"])
    def test_latest_diff_json(self, json_flag):
        """
        Test "recipy latest --diff -j|--json".
        """
        exit_code, _ = self.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--diff", json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        helpers.compare_json_logs(json_log, db_log)
        assert json_log["diff"] == "", "Expected 'diff' to be empty"

        self.modify_script()

        exit_code, _ = self.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        exit_code, stdout = process.execute_and_capture(
            "recipy", ["latest", "--diff", json_flag])
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        assert len(stdout) > 0, "Expected stdout"
        json_log = json.loads(" ".join(stdout))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        helpers.compare_json_logs(json_log, db_log)
        assert json_log["diff"] != "", "Expected 'diff' to be non-empty"
        # Search for diff-related mark-up.
        helpers.search_regexps(json_log["diff"], self.get_diff_regexps())

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
        exit_code, _ = self.run_script()
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
        helpers.compare_json_logs(json_log, db_log)

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
        exit_code, _ = self.run_script()
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
        exit_code, _ = self.run_script()
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
        for _ in range(num_runs):
            exit_code, _ = self.run_script()
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
        exit_code, _ = self.run_script()
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
        helpers.compare_json_logs(json_log[0], db_log)

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
        exit_code, _ = self.run_script()
        assert exit_code == 0, ("Unexpected exit code " + str(exit_code))
        db_log, _ = helpers.get_log(recipyenv.get_recipydb())
        unique_id = db_log["unique_id"]
        pattern = self.get_search(search_flag, unique_id)
        args = ["search"]
        args.extend(pattern)
        args.append("value")
        args.append(json_flag)
        exit_code, _ = process.execute_and_capture("recipy", args)
        assert exit_code == 1, ("Unexpected exit code " + str(exit_code))
