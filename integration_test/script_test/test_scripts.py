"""
recipy test case runner.

Run tests to check that recipy logs information on input and output
functions invoked by scripts which use packages that recipy has been
configured to log.

Tests are specified using a [YAML](http://yaml.org/) (YAML Ain't
Markup Language) configuration file. YAML syntax is:

* `---` indicates the start of a document.
* `:` denotes a dictionary. `:` must be followed by a space.
* `-` denotes a list.

The test configuration file has format:

    ---
    SCRIPT:
    - libraries: [LIBRARY, LIBRARY, ... ]
      arguments: [..., ..., ...]
      inputs: [INPUT, INPUT, ...]
      outputs: [OUTPUT, OUTPUT, ...]
    - libraries: [LIBRARY, LIBRARY, ... ]
      arguments: [..., ..., ...]
      inputs: [INPUT, INPUT, ...]
      outputs: [OUTPUT, OUTPUT, ...]
    - ...
    SCRIPT:
    ...

where each script to be tested is defined by:

* 'SCRIPT': script name, with a relative or absolute path
* One or more test cases, each of which defines:
  - 'libraries':  e.g. ['numpy']. A list of one or more libraries used
    by the script, and which are expected to be logged by recipy, when
    the script is run with the given arguments. The list may contain
    either generic names e.g. 'numpy' (compatible with any version of
    numpy) or version qualified names e.g. 'numpy v1.11.1' (compatible
    with numpy v1.11.1+).
  - 'arguments': e.g. ['loadtxt'], ['savetxt']. A list of arguments to
    be passed to the script. If none, then this can be omitted.
  - 'inputs': e.g. ['data.csv']. A list of zero or more input files
    which the script will read, and which are expected to be logged by
    recipy, when running the script with the arguments. If none, then
    this can be omitted.
  - 'outputs': e.g. ['data.csv']. A list of zero or more output files
    which the script will write, and which are expected to be logged
    by recipy, when running the script with the arguments. If none,
    then this can be omitted.

For example:

    ---
    test_numpy.py:
    - libraries: [numpy]
      arguments: [loadtxt]
      inputs: [input.csv]
    - libraries: [numpy]
      arguments: [savetxt]
      outputs: [output.csv]
    - libraries: [numpy]
      arguments: [load_and_save_txt]
      inputs: [input.csv]
      outputs: [output.csv]

It is up to the developer to ensure the 'libraries', 'input' and
'output' lists correctly record the libraries, input and output files
that it is expected recipy will log when the script is run with the
given arguments.

The test configuration file is provided via an environment variable,
'RECIPY_TEST_CONFIG'. If undefined, then a default of
'integration_test/script_test/recipy.yml' is assumed.
"""

import os
import os.path
import pytest

from integration_test.database import DatabaseError
from integration_test import environment
from integration_test.file_utils import load_file
from integration_test import helpers
from integration_test import recipy_environment as recipyenv


TEST_CONFIG_ENV = "RECIPY_TEST_CONFIG"
"""
Environment variable holding recipy test configuration file name
"""

DEFAULT_CONFIG = "integration_test/script_test/recipy.yml"
""" Default recipy test configuration file name """


def get_test_cases():
    """
    py.test callback to associate each test script with its test
    cases. This function:

    * Gets the test configuration file name from the environment
      variable 'RECIPY_TEST_CONFIG'. If undefined, then a default of
      'integration_test/script_test/recipy.yml' is assumed.
    * Loads the test configuration file.
    * Associates each test script in the test configuration with each
      of its individual test cases using get_script_test_cases.

    py.test parameterized tests will generate one test function per
    tuple.

    :return: test cases
    :rtype: list of (str or unicode, dict)
    """
    config_file = helpers.get_environment_value(TEST_CONFIG_ENV,
                                                DEFAULT_CONFIG)
    configuration = load_file(config_file)
    return get_script_test_cases(configuration)


def get_script_test_cases(configuration):
    """
    Associates each test script in the test configuration with each of
    its individual test cases.

    This function takes a test configuration, a dictionary indexed by
    scripts, each of which has an associated list of one or more test
    cases (each of which are a dictionary of 'libraries', 'arguments',
    'inputs' and 'outputs'), and creates a list of tuples (script,
    test_case), where test_case is the individual test case for the
    script.

    :param configuration: Test case configuration
    :type dict: dict of list of dict
    :return: test cases
    :rtype: list of (str or unicode, dict)
    """
    script_test_cases = []
    for script in configuration:
        test_cases = configuration[script]
        for test_case in test_cases:
            script_test_cases.append((script, test_case))
    return script_test_cases


def get_test_case_id(script_test_case):
    """
    py.test callback to generate test case function names.

    Function names are of form 'script:arguments' where 'arguments'
    is formed by concatenating the 'arguments' entry for a script's
    test case and removing all spaces.

    For example, for a script 'run_numpy.py' and a test case with
    ''arguments':[ 'loadtxt' ]' the test case name is
    'run_numpy.py:loadtxt'.

    :param script_test_case: Script plus test case configuration
    :type script_test_case: (str or unicode, dict)
    :return: Test case name
    :rtype: str or unicode
    """
    [script, test_case] = script_test_case
    arguments_str = [str(argument) for argument in test_case["arguments"]]
    arguments_str = "".join(arguments_str).replace(" ", "_")
    test_case_name = str(script) + ":" + arguments_str
    return test_case_name


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
        :param test_case: test case configuration
        :type test_case: dict
        """
        number_of_logs = 0
        try:
            number_of_logs =\
               helpers.get_number_of_logs(recipyenv.get_recipydb())
        except DatabaseError:
            # Database may not exist if running tests for first time so
            # give benefit of doubt at this stage and assume running script
            # will bring it into life.
            pass
        libraries = test_case[TestCaseRunner.LIBRARIES]
        if TestCaseRunner.ARGUMENTS in test_case:
            arguments = test_case[TestCaseRunner.ARGUMENTS]
        else:
            arguments = []
        # TODO Clean up, convert from:
        # python integration_test/script_test/run_numpy.py
        # to:
        # python -m integration_test.script_test.run_numpy
        script_path = os.path.join(test_cases_directory, script)
        script_module = os.path.splitext(script_path)[0]
        script_module = script_module.replace("/", ".")
        script_module = script_module.replace("\\", ".")
        cmd = ["-m", script_module] + arguments
        _, _ = helpers.execute_python(cmd, 0)
        # Validate recipy database
        log, _ = helpers.get_log(recipyenv.get_recipydb())
        # Number of logs
        new_number_of_logs =\
            helpers.get_number_of_logs(recipyenv.get_recipydb())
        assert new_number_of_logs == (number_of_logs + 1),\
            ("Unexpected number of logs " + new_number_of_logs)
        # Script that was invoked
        self.check_script(script_path, log["script"],
                          arguments, log["command_args"])
        # Libraries
        self.check_libraries(libraries, log["libraries"])
        # Inputs and outputs (local filenames only)
        self.check_input_outputs(test_case,
                                 TestCaseRunner.INPUTS,
                                 log["inputs"])
        self.check_input_outputs(test_case,
                                 TestCaseRunner.OUTPUTS,
                                 log["outputs"])
        # Dates
        self.check_dates(log["date"], log["exit_date"])
        # Execution environment
        self.check_environment(log["command"], log["environment"])
        # Miscellaneous
        assert environment.get_user() == log["author"], "Unexpected author"
        assert log["description"] == "", "Unexpected description"
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

    @pytest.mark.parametrize("script_test_case",
                             get_test_cases(),
                             ids=get_test_case_id)
    def test_scripts(self, script_test_case):
        """
        Run a test defined in the recipy test configuration.

        :param script_test_case: Script and a single test case for
         that script
        :type script_test_case: (str or unicode, dict)
        """
        (script, test_case) = script_test_case
        print("\nTest case: ")
        print(test_case)
        # TODO resolve use of this path
        self.run_test_case("integration_test/script_test",
                           script,
                           test_case)
