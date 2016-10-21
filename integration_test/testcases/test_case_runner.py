"""
recipy test case runner.
"""

import os
import os.path
import shutil
import tempfile

from integration_test import environment
from integration_test.file_utils import load_file
from integration_test import helpers
from integration_test import process
from integration_test import recipy_environment as recipyenv


class TestCaseRunner(object):

    LIBRARIES = "libraries"
    """ Test case configuration key. """
    ARGUMENTS = "arguments"
    """ Test case configuration key. """
    INPUTS = "inputs"
    """ Test case configuration key. """
    OUTPUTS = "outputs"
    """ Test case configuration key. """
    
    def run_test_case(self, test_cases_directory, script, test_case):
        """
        Run a single test case. This runs a test case script
        using arguments in test_case and validates that recipy
        has logged information about the script, also using data
        in test_case. test_case is assumed to have the following
        entries:

        * 'libraries': a list of one or more libraries
             e.g. ['numpy']. 
        * 'arguments': a list of script arguments e.g. ['loadtxt'],
          ['savetxt']. If none, then this can be omitted.
        * 'inputs': a list of zero or more input files which running
              the script with the argument will read e.g. ['data.csv']. If
          none, then this can be omitted.
        * 'outputs': a list of zero or more output files which running
              the script with the argument will write e.g. ['data.csv']. If
          none, then this can be omitted.

        :param test_cases_directory: directory with test cases
        :type test_cases_directory: str or unicode
        :param script: test case script e.g. 'run_numpy.py'
        :type script: str or unicode
        :param test_case: test case specification
        :type test_case: dict
        """
        libraries = test_case[TestCaseRunner.LIBRARIES]
        if TestCaseRunner.ARGUMENTS in test_case:
            arguments = test_case[TestCaseRunner.ARGUMENTS]
        else:
            arguments = []
        # python integration_test/testcases/run_numpy.py
        # python -m integration_test.testcases.run_numpy
        script_path = os.path.join(test_cases_directory, script)
        print(("Script path: ", script_path))
        script_module = os.path.splitext(script_path)[0]
        script_module = script_module.replace("/", ".")
        script_module = script_module.replace("\\", ".")
        cmd = ["-m", script_module] + arguments
        print(("Command: ", cmd))
        exit_code, stdout = process.execute_and_capture(
            environment.get_python_exe(),
            cmd)
        print(("Exit code: ", exit_code))
        print(("Standard output: ", stdout))
        # Validate recipy database.
        if TestCaseRunner.INPUTS in test_case:
            inputs = test_case[TestCaseRunner.INPUTS]
        else:
            inputs = []
        if TestCaseRunner.OUTPUTS in test_case:
            outputs = test_case[TestCaseRunner.OUTPUTS]
        else:
            outputs = []
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        print(log["script"])
        assert os.path.abspath(script_path) == log["script"],\
            "Unexpected script"
        print(log["command_args"])
        assert " ".join(arguments) == log["command_args"],\
               "Unexpected command_args"
        print(log["author"])
        assert environment.get_user() == log["author"], "Unexpected author"
        print(log["description"])
        assert "" == log["description"], "Unexpected description"
        print(log["warnings"])
        assert [] == log["warnings"], "Unexpected warnings"
        print(log["command"])
        assert environment.get_python_exe() == log["command"],\
               "Unexpected command"
        print(log["date"])
        print(log["exit_date"])
        try:
            start_date = environment.get_tinydatestr_as_date(log["date"])
        except ValueError as e:
            assert False, "date is not a valid date string"
        try:
            exit_date = environment.get_tinydatestr_as_date(log["exit_date"])
        except ValueError as e:
            assert False, "end_date is not a valid date string"
        assert start_date <= exit_date, "date is not before exit_date"
        # TODO There is only one new run in the database i.e.
        # number of logs has increased by 1.
        # TODO 'unique_id' matches that returned from the database.
        print(log["unique_id"])
        # TODO need library versions
        print(log["libraries"])
        # assert libraries == log["libraries"], "Unexpected libraries"
        # TODO equal 'inputs'
        print(log["inputs"])
        # TODO equal 'outputs'
        print(log["outputs"])
        # TODO 'date' and 'exit_date' are valid dates
        # TODO record the current year, month and day
        # TODO 'date' <= 'exit_date'.
        # * 'environment' holds the operating system and version of the current Python interpreter.
        print(log["environment"])

    def test_case(self):
        specification = load_file("integration_test/testcases/recipy.yml")
        print(("Specification: ", specification))
        for script in specification:
            print(("Script: ", script))
            test_cases = specification[script]
            # Just run one for now TODO remove
#            test_cases = [test_cases[0]]

            for test_case in test_cases:
                    self.run_test_case("integration_test/testcases",
                                       script,
                                       test_case)
        # TODO switch to parameterised tests and remove try-except block
