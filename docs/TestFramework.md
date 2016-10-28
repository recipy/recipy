# recipy test framework 

recipy's test framework is in `integration_test`. The test framework
has been designed to run under both Python 2.7+ and Python 3+.

---

## Running tests with py.test

The tests use the [py.test](http://pytest.org) test framework, and are
run using its `py.test` command. Useful `py.test` flags and
command-line options include:

* `-v`: increase verbosity. This shows the name each test function
  that is run.
* `-s`: show any output to standard output.
* `-rs`: show extra test summary information for tests that were
  skipped.
* `--junit-xml=report.xml`: create a JUnit-style test report in the
  file `report.xml`. 

---

## Running general tests

To run tests of recipy's command-line functions, run:

```
py.test -v integration_test/test_recipy.py
```

To run tests of recipy's `.recipyrc` configuration file, run:

```
py.test -v integration_test/test_recipyrc.py
```

To run tests of recipy invocations using `python -m recipy script.py`,
run:

```
py.test -v integration_test/test_m_flag.py
```

---

## Running package-specific tests

To run tests that check recipy logs information about packages it has
been configured to log, run:

```
py.test -v -rs integration_test/test_packages.py
```

**Note:** this assumes that all the packages have been installed.

To run a single test, provide the name of the test, for example:

```
$ py.test -v -rs integration_test/test_packages.py::test_scripts\[run_numpy_py_loadtxt\]
```

**Note:** `[` and `]` need to be prefixed by `\`.

Package-specific tests use a test configuration file located in
`integration_test/config/test_packages.yml`.

You can specify a different test configuration file using a
`RECIPY_TEST_CONFIG` environment variable. For example: 

```
RECIPY_TEST_CONFIG=test_my_package.yml py.test -v -rs \
    integration_test/test_packages.py
```

**Note:** the above command should be typed on one line, omitting `\`.

For Windows, run:

```
set RECIPY_TEST_CONFIG=test_my_package.yml
py.test -v -rs integration_test\test_packages.py
```

### Test configuration file

The test configuration file is written in [YAML](http://yaml.org/)
(YAML Ain't Markup Language). YAML syntax is:

* `---` indicates the start of a document.
* `:` denotes a dictionary. `:` must be followed by a space.
* `-` denotes a list.

The test configuration file has format:

```
---
script: SCRIPT
standalone: True | False
libraries: [LIBRARY, LIBRARY, ... ]
test_cases:
- libraries: [LIBRARY, LIBRARY, ... ]
  arguments: [..., ..., ...]
  inputs: [INPUT, INPUT, ...]
  outputs: [OUTPUT, OUTPUT, ...]
- libraries: [LIBRARY, LIBRARY, ... ]
  arguments: [..., ..., ...]
  inputs: [INPUT, INPUT, ...]
  outputs: [OUTPUT, OUTPUT, ...]
  skip: "Known issue with recipy" 
- etc
---
script: SCRIPT
etc
```

Each script to be tested is defined by:

* `SCRIPT`: Python script, with a relative or absolute path. For
  recipy sample scripts (see below), the script is assumed to be in a
  sub-directory `integration_test/packages`.
* `standalone`: is the script a standalone script? If `False`, or if
  omitted, then the script is assumed to be a recipy sample script
  (see below).
* `libraries`: A list of zero or more Python libraries used by the
  script, which are expected to be logged by recipy when the script
  is run regardless of arguments (i.e. any libraries common to all
  test cases). If none, then this can be omitted.

Each script also has one or more test cases, each of which defines:

* `libraries`: A list of zero or more Python libraries used by the
  script, which are expected to be logged by recipy when the script
  is run with the given arguments for this test case. If none, then
  this can be omitted.
* `arguments`: A list of arguments to be passed to the script. If
  none, then this can be omitted.
* `inputs`: A list of zero or more input files which the script will
  read, and which are expected to be logged by recipy when running
  the script with the arguments. If none, then this can be omitted.
* `outputs`: A list of zero or more output files which the script
  will write, and which are expected to be logged by recipy when
  running the script with the arguments. If none, then this can be
  omitted.
* `skip`: An optional value. If present this test case is marked as
  skipped. The value is the reason for skipping the test case.

For example:

```
---
script: run_numpy.py
libraries: [numpy]
test_cases:
- arguments: [loadtxt]
  inputs: [input.csv]
- arguments: [savetxt]
  outputs: [output.csv]
- arguments: [load_and_save_txt]
  inputs: [input.csv]
  outputs: [output.csv]
---
script: "/home/users/user/run_my_script.py"
standalone: True
test_cases:
- arguments: [ ]
  libraries: [ numpy ]
  outputs: [ data.csv ]
---
script: run_nibabel.py
libraries: [ nibabel ]
test_cases:
- arguments: [ analyze_from_filename ]
  inputs: [ analyze_image ]
- arguments: [ analyze_to_filename ]
  outputs: [ out_analyze_image ]
- arguments: [ minc1_from_filename ]
  inputs: [ minc1_image ]
- arguments: [ minc1_to_filename ]
  outputs: [ out_minc1_image ]
  skip: "nibabel.minc1.Minc1Image.to_filename raises NotImplementedError"
```

There may be a number of entries for a single script, if desired. For
example:

```
---
script: run_numpy.py
libraries: [numpy]
test_cases:
- arguments: [loadtxt]
  inputs: [input.csv]
- arguments: [savetxt]
  outputs: [output.csv]
---
script: run_numpy.py
libraries: [numpy]
test_cases:
- arguments: [load_and_save_txt]
  inputs: [input.csv]
  outputs: [output.csv]
```

It is up to you to ensure the `library`, `input` and `output` file
names record the libraries, input and output files used by the
associated script, and which you expect to be logged by recipy.

Comments can be added to configuration files, prefixed by `#`, for
example:

```
# This is a comment
```

---

## How the test framework uses test configuration files

A test configuration file is used to auto-generate test functions for
each test case using py.test's support for
[parameterization](http://doc.pytest.org/en/latest/parametrize.html).

In the first example above, 8 test functions are created, 3 for
`run_numpy.py` and 1 for `run_my_scripy.py` and 4 for `run_nibabel.py`
(of which 1 is marked to be skipped. In the second example, 3 test
functions are created, 2 for the first group of `run_numpy.py` test
cases and 1 for the second group.

Test function names are auto-generated according to the following
template:

```
test_scripts[SCRIPT_ARGUMENTS]
```

where `SCRIPT` is the `script` value and arguments the `argument`
values, concatenated using underscores (`_`) and with all forward
slashes, backslashes, colons, semi-colons and spaces also replaced by
`_`. For example, `test_scripts[run_nibabel_py_analyze_from_filename]`.

The test framework runs the script with its arguments as follows. For
recipy sample scripts:

```
python -m integration_test.package.SCRIPT ARGUMENTS
```

For scripts marked `standalone: True`:

```
python SCRIPT ARGUMENTS
```

Once the script has run, the test framework carries out the following
checks on the recipy database:

* There is only one new run in the database i.e. number of logs has
  increased by 1.
* `script` refers to the same file as the `script`.
* `command_args` matches the test case's `arguments`.
* `libraries` matches all the test case's `libraries` and all the
  `libraries` common to all test case's for a script, and the
  recorded versions match the versions used when `script` was run.
* `inputs` match the test case's `inputs` (in terms of local file
  names).
* `outputs` match test case's `outputs` (in terms of local file
  names).
* `date` is a valid date.
* `exit_date` is a valid date and is <= `date`.
* `command` holds the current Python interpreter.
* `environment` holds the operating system and version of the current
  Python interpreter.
* `author` holds the current user.
* `description` is empty.

### recipy sample scripts

`integration_test/packages` has a collection of package-specific
scripts. Each script corresponds to one package logged by recipy. Each
script has a function that invokes each of the input/output functions
of a specific package logged by recipy. For example, `run_numpy.py`
has functions that invoke:

* `numpy.loadtxt`
* `numpy.savetxt`
* `numpy.fromfile`
* `numpy.save`
* `numpy.savez`
* `numpy.savez_compressed`
* `numpy.genfromtxt`

Each function is expected to invoke input and/or output functions
using one or more functions which recipy can log.

Input and output files are the responsibility of each script
itself. It can either create its own input and output files, or
read these in from somewhere (but it is not expected that the caller
(i.e. the test framework) create these.

Each test class has access to its own directory, via a
`self.current_dir` field. It can use this to access any files it
needs within the current directory or, by convention, within a
sub-directory of `data` (for example `run_numpy.py` assumes a
`data/numpy` sub-directory).

These scripts consist of classes that inherit from
`integration_test.base.Base` which provides sub-classes with a simple
command-line interface which takes a function name as argument and, if
that function is provided by the script's class (and takes no
arguments beyond `self`), invokes that function. For example:

```
python SCRIPT.py FUNCTION
```

A sample script can be run as follows:

```
python -m integration_test.packages.SCRIPT FUNCTION
```

For example:

```
python -m integration_test.packages.run_numpy loadtxt
```

`test_packages.py` assumes that if it is given a relative path to a
script, then that script is in `integration_test/packages` and will
create this form of invocation.

**Running scripts as modules**

Note that the script needs to be specified as a module that is run as
a script (the `-m` flag). Running it directly as a script e.g.

```
$ python integration_test/packages/run_numpy.py loadtxt
```

will fail:

```
Traceback (most recent call last):
  File "integration_test/packages/run_numpy.py", line 17, in <module>
    from integration_test.packages.base import Base
ImportError: No module named 'integration_test.packages'
```

For the technical detail of why this is so, please see [Execution of
Python code with -m option or
not](http://stackoverflow.com/questions/22241420/execution-of-python-code-with-m-option-or-not).

---

## Providing a test configuration for any script

A recipy test configuration can be written for any script that uses
recipy. For example, to test a script that uses `numpy.loadtxt` you
could write a configuration file which specifies:

* Full path to your script.
* Command-line arguments to be passed to your script.
* Libraries you expect to be logged by recipy.
* Local names of input files you expect to be logged by recipy.
* Local names of output files you expect to be logged by recipy.

For example, `my_tests.yml`:

```
---
script: "/home/ubuntu/sample/run_numpy.py"
standalone: True
test_cases:
- arguments: [ "/home/ubuntu/data/data.csv",
               "/home/ubuntu/data/out.csv" ]
  libraries: [ numpy ]
  inputs: [ data.csv ]
  outputs: [ out.csv ]
```

You can run this as follows:

```
RECIPY_TEST_CONFIG=my_tests.yml py.test -v -rs \
    integration_test/test_packages.py
```

The output might look like

```
============================= test session starts ==============================
platform linux2 -- Python 2.7.12, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /home/ubuntu/anaconda2/bin/python
cachedir: .cache
rootdir: /home/ubuntu/recipy, inifile: 
collected 1 items 

integration_test/test_packages.py::test_scripts[run_numpy_py__home_ubuntu_data_data_csv__home_ubuntu_data_out_csv] PASSED

=========================== 1 passed in 4.39 seconds ===========================
```

If using Anaconda and Git Bash on Windows, the file might look like:

```
---
script: "c:/Users/mjj/Local\ Documents/sample/run_numpy.py"
standalone: True
test_cases:
- arguments: [ "c:/Users/mjj/Local\ Documents/data/data.csv",
               "c:/Users/mjj/Local\ Documents/data/out.csv" ]
  libraries: [ numpy ]
  inputs: [ data.csv ]
  outputs: [ out.csv ]
```

Note the escaped spaces in the path.

---

## Test framework limitations

The test framework does not support filtering tests depending upon
which versions of packages are being tested e.g. specific versions of
numpy or matplotlib. The test framework is designed to run tests
within a single execution environment: a Python interpreter and a set
of installed libraries.

If wishing to test different versions of packages then this could be
done by:

* Writing a Python script that invokes input/output functions of that
  package.
* Writing a test configuration file that just runs that script.
* Setting up a test environment (e.g. as part of a Travis CI or
  AppVeyor configuration file) that installs the specific package and
  runs `py.test integration_test/test_packages.py` using the 
  test configuration file.

`test_recipy.py` does not validate whether multiple test results are
returned by `recipy search -i`.

---

## recipy dependencies

The test framework has no dependencies on any other part of the recipy
repository: it uses recipy as if it were a stand-alone tool and
queries the recipy database directly.

---
