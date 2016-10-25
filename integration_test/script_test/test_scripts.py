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
    NAME:
      script: SCRIPT
      [standalone: True|False]
      test_cases:
      - libraries: [LIBRARY, LIBRARY, ... ]
        arguments: [..., ..., ...]
        inputs: [INPUT, INPUT, ...]
        outputs: [OUTPUT, OUTPUT, ...]
      - libraries: [LIBRARY, LIBRARY, ... ]
        arguments: [..., ..., ...]
        inputs: [INPUT, INPUT, ...]
        outputs: [OUTPUT, OUTPUT, ...]
      - ...
    NAME:
      script: SCRIPT
      ...

where each script to be tested is defined by:

* 'NAME': human-readable name for a set of test cases.
* 'SCRIPT': script, with a relative or absolute path. For recipy
  sample scripts the path is assumed to be relative to
  "integration_test/script_test".
* 'standalone': is the script a standalone script? If "False" or if
  omitted then the script is assumed to be a recipy sample script,
  runnable via the command 'python -m
  integration_test.script_test.SCRIPT'.
* One or more test cases, each of which defines:
  - 'libraries': A list of one or more libraries used by the script,
    and which are expected to be logged by recipy, when the script is
    run with the given arguments. The list may contain either generic
    names e.g. 'numpy' (compatible with any version of numpy) or
    version qualified names e.g. 'numpy v1.11.1' (compatible with
    numpy v1.11.1+).
  - 'arguments': A list of arguments to be passed to the script. If
    none, then this can be omitted.
  - 'inputs': A list of zero or more input files which the script will
    read, and which are expected to be logged by recipy, when running
    the script with the arguments. If none, then this can be omitted.
  - 'outputs': A list of zero or more output files which the script
    will write, and which are expected to be logged by recipy, when
    running the script with the arguments. If none, then this can be
    omitted.

For example:

    ---
    numpy:
      script: run_numpy.py
      cases:
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
    custom:
      script: "/home/users/user/run_my_script.py"
      standalone: True
      cases:
      - arguments: [ ]
        libraries: [ numpy ]
        outputs: [ data.csv ]

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
from integration_test.file_utils import load_yaml
from integration_test import helpers
from integration_test import recipy_environment as recipyenv

SCRIPT = "script"
""" Test case configuration key. """

STANDALONE = "standalone"
""" Test case configuration key. """

TEST_CASES = "test_cases"
""" Test case configuration key. """

LIBRARIES = "libraries"
""" Test case configuration key. """

ARGUMENTS = "arguments"
""" Test case configuration key. """

INPUTS = "inputs"
""" Test case configuration key. """

OUTPUTS = "outputs"
""" Test case configuration key. """

TEST_CONFIG_ENV = "RECIPY_TEST_CONFIG"
"""
Environment variable holding recipy test configuration file name
"""

DEFAULT_CONFIG = "integration_test/script_test/recipy.yml"
""" Default recipy test configuration file name """

DEFAULT_SAMPLES = "integration_test/script_test"
""" Default recipy sample scripts directory """


def get_test_cases():
    """
    py.test callback to associate each test script with its test
    cases. This function:

    * Gets the test configuration file name from the environment
      variable 'RECIPY_TEST_CONFIG'. If undefined, then a default of
      'integration_test/script_test/recipy.yml' is assumed.
    * Loads the test configuration file.
    * Creates a list of standalone tuples, each representing one
      test case, using get_script_test_cases.

    py.test parameterized tests will generate one test function per
    tuple.

    :return: test cases
    :rtype: list of (str or unicode, str or unicode, str or unicode, dict)
    """
    config_file = helpers.get_environment_value(TEST_CONFIG_ENV,
                                                DEFAULT_CONFIG)
    configuration = load_yaml(config_file)
    return get_script_test_cases(configuration, DEFAULT_SAMPLES)


def get_script_test_cases(configurations, recipy_samples_directory):
    """
    Creates a list of standalone tuples, each representing one test
    case.

    This function takes a test configuration, a dictionary indexed by
    test names, each of which has a 'script', optional 'standalone'
    flag, and 'cases', a list of one or more test cases (each of which
    is a dictionary of 'libraries', 'arguments', 'inputs' and
    'outputs').

    It returns a list of tuples (name, script path, command, test
    case) where:

    * name is the name of a collection of test cases associated with a
      script.
    * script_path is the path to the script.
      - If the test configuration has a 'standalone' value of "False",
        or no such value, then the script is assumed to be a recipy
        sample script in "integration_test/script_test/script".
      - Otherwise, the 'script' configuration value is used as-is.
    * commmand is the command-line invocation that will be used to run
      the script (not including "python" or any arguments, which are
      test-case specific):
      - If the test configuration has a 'standalone' value of "False",
        or no such value, then the command to run the script is
        assumed to be "-m integration_test.script_test.SCRIPT"
      - Otherwise, the 'script' configuration value is used as-is.
    * test_case is a single test case configuration.

    :param configurations: Test case configurations
    :type dict: list of dict
    :param recipy_samples_directory: directory with recipy samples
    :type recipy_samples_directory: str or unicode
    :return: test cases
    :rtype: list of (str or unicode, str or unicode, str or unicode, dict)
    """
    [configuration] = configurations
    test_cases = []
    for name in configuration:
        named_config = configuration[name]
        script = named_config[SCRIPT]
        if STANDALONE not in named_config:
            # recipy sample test
            script_path = os.path.join(recipy_samples_directory, script)
            # e.g. integration_test/script_test/run_numpy.py
            script_module = os.path.splitext(script_path)[0]
            # e.g. integration_test/script_test/run_numpy
            script_module = script_module.replace("/", ".")
            script_module = script_module.replace("\\", ".")
            # e.g. integration_test.script_test.run_numpy
            command = ["-m", script_module]
            # e.g. -m integration_test.script_test.run_numpy
        else:
            script_path = script
            command = [script]
        for test_case in named_config[TEST_CASES]:
            test_cases.append((name, script_path, command, test_case))
    return test_cases


def get_test_case_function_name(script_test_case):
    """
    py.test callback to generate test case function names.

    Function names are of form 'name_arguments' where 'arguments'
    is the 'arguments' for the test case converted to strings,
    joined and with all forward slashes, backslashes, colons,
    semi-colons and spaces replaced by '_'.

    :param script_test_case: Name, script path, command, test case
     specification - consistent with a tuple from
     get_script_test_cases.
    :type script_test_case: (str or unicode, str or unicode, str or
     unicode, dict)
    :return: Test case function name
    :rtype: str or unicode
    """
    [name, _, _, test_case] = script_test_case
    arguments_str = [str(argument) for argument in test_case[ARGUMENTS]]
    arguments_str = "_".join(arguments_str)
    for char in [" ", "\\", "/", ":", ";"]:
        arguments_str = arguments_str.replace(char, "_")
    function_name = name + "_" + arguments_str
    return function_name


class TestCaseRunner(object):
    """
    recipy test case runner.
    """

    def run_test_case(self, name, script_path, command, test_case):
        """
        Run a single test case. This runs a test case script
        using arguments in test_case and validates that recipy
        has logged information about the script, also using data
        in test_case.

        test_case is assumed to have the following
        entries:

        * 'libraries': a list of one or more libraries
          e.g. ['numpy'].
        * 'arguments': a list of script arguments e.g. ['loadtxt'],
          ['savetxt']. If none, then this can be omitted.
        * 'inputs': a list of zero or more input files which running
          the script with the argument will read e.g. ['data.csv']. If
          none, then this can be omitted.
        * 'outputs': a list of zero or more output files which running
          the script with the argument will write
          e.g. ['data.csv']. If none, then this can be omitted.

        :param name: Name of a collection of test cases associated with a
         script.
        :type name: str or unicode
        :param script_path: Path to the script.
        :type script_path: str or unicode
        :param commmand: is the command-line invocation that will be
          used to run the script (not including "python" or any
         arguments, which are test-case specific).
        :type command: str or unicode
        :param test_case: Test case configuration.
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
        libraries = test_case[LIBRARIES]
        if ARGUMENTS in test_case:
            arguments = test_case[ARGUMENTS]
        else:
            arguments = []
        # Execute script
        _, _ = helpers.execute_python(command + arguments, 0)
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
                                 INPUTS,
                                 log["inputs"])
        self.check_input_outputs(test_case,
                                 OUTPUTS,
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
        # Rather than simple equality check, see if paths refer to the
        # same file. Avoids problems with forward vs backslashes and
        # inconsistent paths on Anaconda Python on Windows, for
        # example.
        assert os.path.samefile(script, logged_script)
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
            else:
                raise ConfigError((
                    "Library {} is not installed".format(library)))

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
                             ids=get_test_case_function_name)
    def test_scripts(self, script_test_case):
        """
        Run a test defined in the recipy test configuration.

        :param script_test_case: Name, script path, command, test case
         specification - consistent with a tuple from
         get_script_test_cases.
        :type script_test_case: (str or unicode, str or unicode, str or
         unicode, dict)
        """
        (name, script_path, command, test_case) = script_test_case
        self.run_test_case(name, script_path, command, test_case)


class ConfigError(Exception):
    """Test configuration error."""

    def __init__(self, message, exception=None):
        """Create error.

        :param message: Message
        :type message: str or unicode
        :param exception: Exception
        :type value: Exception
        """
        super(ConfigError, self).__init__()
        self._message = message
        self._exception = exception

    def __str__(self):
        """Get error as a formatted string.

        :return: formatted string
        :rtype: str or unicode
        """
        message = self._message
        if self._exception is not None:
            message += " : " + str(self._exception)
        return repr(message)

    @property
    def exception(self):
        """Get exception.

        :param exception: Exception
        :type value: Exception
        """
        return self._exception
