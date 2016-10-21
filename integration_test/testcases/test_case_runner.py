"""
recipy test case runner.
"""

import os
import os.path

from integration_test import environment
from integration_test.file_utils import load_file
from integration_test import helpers
from integration_test import process
from integration_test import recipy_environment as recipyenv


class TestCaseRunner(object):
    """
    recipy test case runner.
    """

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
          the script with the argument will read
          e.g. ['data.csv']. If none, then this can be omitted.
        * 'outputs': a list of zero or more output files which running
          the script with the argument will write
          e.g. ['data.csv']. If none, then this can be omitted.

        :param test_cases_directory: directory with test cases
        :type test_cases_directory: str or unicode
        :param script: test case script e.g. 'run_numpy.py'
        :type script: str or unicode
        :param test_case: test case specification
        :type test_case: dict
        """
        number_of_logs = helpers.get_number_of_logs(recipyenv.get_recipydb())
        print(("Number of logs: ", number_of_logs))
        libraries = test_case[TestCaseRunner.LIBRARIES]
        if TestCaseRunner.ARGUMENTS in test_case:
            arguments = test_case[TestCaseRunner.ARGUMENTS]
        else:
            arguments = []
        # Convert from:
        # python integration_test/testcases/run_numpy.py
        # to:
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

        # Validate recipy database
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        # Number of logs
        new_number_of_logs =\
            helpers.get_number_of_logs(recipyenv.get_recipydb())
        print(("Number of logs: ", new_number_of_logs))
        assert new_number_of_logs == (number_of_logs + 1),\
            ("Unexpected number of logs " + new_number_of_logs)
        # Script that was invoked
        print((log["script"]))
        print((log["command_args"]))
        self.check_script(script_path, log["script"],
                          arguments, log["command_args"])
        # Libraries
        print((log["libraries"]))
        self.check_libraries(libraries, log["libraries"])
        # Inputs and outputs (local filenames only)
        print((log["inputs"]))
        self.check_input_outputs(test_case,
                                 TestCaseRunner.INPUTS,
                                 log["inputs"])
        print((log["outputs"]))
        self.check_input_outputs(test_case,
                                 TestCaseRunner.OUTPUTS,
                                 log["outputs"])
        # Dates
        print((log["date"]))
        print((log["exit_date"]))
        self.check_dates(log["date"], log["exit_date"])
        # Execution environment
        print((log["command"]))
        print((log["environment"]))
        self.check_environment(log["command"], log["environment"])
        # Miscellaneous
        print((log["author"]))
        assert environment.get_user() == log["author"], "Unexpected author"
        print((log["description"]))
        assert log["description"] == "", "Unexpected description"
        print((log["warnings"]))
        assert [] == log["warnings"], "Unexpected warnings"

    def check_script(self, script, logged_script,
                     arguments, logged_arguments):
        """
        Check script and arguments logged by recipy.

        :param script: Script specified in test configuration
        :type script: str or unicode
        :param logged_script: Script logged by recipy
        :type logged_script: str or unicode
        :param arguments: Arguments specified in test configuration
        :type arguments: list
        :param logged_arguments: Arguments logged by recipy
        :type logged_arguments: list
        """
        assert os.path.abspath(script) == logged_script,\
            "Unexpected script"
        assert " ".join(arguments) == logged_arguments,\
               "Unexpected command_args"

    def check_libraries(self, libraries, logged_libraries):
        """
        Check libraries logged by recipy.

        :param libraries: Libraries specified in test configuration
        :type libraries: list of str or unicode
        :param logged_libraries: Libraries logged by recipy
        :type logged_libraries: list of str or unicode
        """
        packages = environment.get_packages()
        for library in libraries:
            if environment.is_package_installed(packages, library):
                version = environment.get_package_version(packages, library)
                library_version = library + " v" + version
                assert library_version in logged_libraries,\
                    ("Could not find library " + library_version)

    def check_dates(self, logged_start_date, logged_end_date):
        """
        Check dates logged by recipy.

        :param logged_start_date: Start date logged by recipy
        :type logged_start_date: str or unicode
        :param logged_end_date: End date logged by recipy
        :type logged_end_date: str or unicode
        """
        try:
            start_date = environment.get_tinydatestr_as_date(logged_start_date)
        except ValueError as _:
            assert False, "date is not a valid date string"
        try:
            exit_date = environment.get_tinydatestr_as_date(logged_end_date)
        except ValueError as _:
            assert False, "end_date is not a valid date string"
        assert start_date <= exit_date, "date is not before exit_date"

    def check_environment(self, logged_command, logged_environment):
        """
        Check environment logged by recipy.

        :param logged_command: Python executable logged by recipy
        :type logged_command: str or unicode
        :param logged_environment: Operating system and Python
        version logged by recipy
        :type logged_environment: list of str or unicore
        """
        assert environment.get_python_exe() == logged_command,\
            "Unexpected command"
        assert environment.get_os() in logged_environment,\
            "Cannot find operating system in environment"
        python_version = "python " + environment.get_python_version()
        assert python_version in logged_environment,\
            "Cannot find Python in environment"

    def check_input_outputs(self, test_case, io_key, logged_io):
        """
        Check inputs/outputs logged by recipy.

        :param test_case: Test case configuration
        :type test_case: dict
        :param io_key: "inputs" or "outputs", key into test_case
        :type io_key: str or unicode
        :param logged_io: Inputs/outputs logged by recipy
        :type logged_io: list
        """
        if io_key in test_case:
            io_files = test_case[io_key]
        else:
            io_files = []
        assert len(io_files) == len(logged_io),\
            ("Unexpected number of " + io_key)
        # Convert logged files to local file names.
        logged_files = [os.path.basename(file_name)
                        for [file_name, _] in logged_io]
        for io_file in io_files:
            assert io_file in logged_files,\
                ("Could not find " + io_key + " " + io_file)

    def test_case(self):
        """
        # TODO switch to parameterised tests
        """
        specification = load_file("integration_test/testcases/recipy.yml")
        print(("Specification: ", specification))
        for script in specification:
            print(("Script: ", script))
            test_cases = specification[script]
            # TODO remove this which ensures just one run is done.
            # test_cases = [test_cases[0]]
            for test_case in test_cases:
                self.run_test_case("integration_test/testcases",
                                   script,
                                   test_case)
