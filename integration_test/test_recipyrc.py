"""
Tests of recipy configuration, provided via 'recipyrc' configuration files.
"""

import os
import os.path
import shutil
import tempfile
import pytest

try:
    from ConfigParser import SafeConfigParser, Error
except:
    from configparser import SafeConfigParser, Error

from .process import execute
from .environment import get_recipy_dir, get_recipydb, get_recipyrc
from .database import TINYDB_PATH, open_db, get_latest_id, get_log, close_db, get_filediffs

class TestRecipyrc:
    """
    Tests of recipy configuration, provided via 'recipyrc'
    configuration files.
    """

    test_script = "run_numpy.py"
    test_input_data = "input.csv"
    test_output_data = "output.csv"
    test_directory = ""
    
    @classmethod
    def run_script(cls):
        """
        Run test_script using Python.

        :return: exit code
        :rtype: int
        """
        return execute("python", [TestRecipyrc.test_script])

    @classmethod
    def update_recipyrc(cls, recipyrc, section, key, value=None):
        """
        Update recipyrc configuration.

        :param recipyrc: recipyrc configuration file
        :type recipyrc: str or unicode
        :param section: configuration section, created if it does not exist
        :type section: str or unicode
        :param key: key
        :type key: str or unicode
        :param value: value, optional for key-only parameters
        :type value: str or unicode
        """
        config = SafeConfigParser(allow_no_value=True)
        config.read(recipyrc)
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, key, value)
        with open(recipyrc, "w") as configfile:
            config.write(configfile)

    @classmethod
    def get_log(cls, recipydb):
        """
        Get the latest log from the database along with its
        'filediffs', if any.
        
        :param recipydb: recipydb path
        :type recipydb: str or unicode
        :return: log
        :rtype: dict
        :return: log and filediffs. If no 'filediffs' then this value
        is None. If no log exists then None is returned.
        :rtype: (dict, dict)
        """
        connection = {TINYDB_PATH: recipydb}
        db = open_db(connection)
        latest = get_latest_id(db)
        (log_number, log) = get_log(db, latest)
        diffs = get_filediffs(db, log_number)
        close_db(db)
        return (log, diffs)

    @classmethod
    def setup_class(cls):
        """
        py.test-compliant setup function, run when module is loaded,
        creates Temp/TMP/run_numpy.py and Temp/TMP/input.csv.
        """
        TestRecipyrc.test_directory = tempfile.mkdtemp(TestRecipyrc.__name__)
        TestRecipyrc.test_script =\
             os.path.join(TestRecipyrc.test_directory,
                          TestRecipyrc.test_script)
        TestRecipyrc.test_output_data =\
             os.path.join(TestRecipyrc.test_directory,
                          TestRecipyrc.test_output_data)
        TestRecipyrc.test_input_data =\
             os.path.join(TestRecipyrc.test_directory,
                          TestRecipyrc.test_input_data)
        with open(TestRecipyrc.test_input_data, "w") as f:
            f.write("1,4,9,16")
            f.write("\n")
        with open(TestRecipyrc.test_script, "w") as f:
            f.write("import recipy")
            f.write("\n")
            f.write("import numpy as np")
            f.write("\n")
            f.write("data = np.array([list(range(4,8))])")
            f.write("\n")
            f.write("np.savetxt(" +
                    str(TestRecipyrc.test_output_data).__repr__() +
                    ", data, delimiter=',')")
            f.write("\n")
            f.write("data = np.loadtxt(" +
                    str(TestRecipyrc.test_input_data).__repr__() +
                    ", delimiter=',')")
            f.write("\n")
            f.write("print(data)")
            f.write("\n")

    @classmethod
    def teardown_class(cls):
        """
        py.test-compliant setup function, run when module is completed,
        deletes Temp/TMP/.
        """
        if os.path.isdir(TestRecipyrc.test_directory):
            shutil.rmtree(TestRecipyrc.test_directory)

    def setup_method(self, method):
        """
        py.test-compliant setup function, run before each test method,
        deletes ~/.recipy.
        As py.test ignores test classes that have __init__ methods,
        an attribute, self.test_files, is defined in this method.

        :param method: Test method
        :type method: function
        """
        recipy_dir = get_recipy_dir()
        if os.path.isdir(recipy_dir):
            shutil.rmtree(recipy_dir)
        os.mkdir(recipy_dir)
        for recipyrc_file in [".recipyrc", "recipyrc"]:
            path = os.path.join(os.getcwd(), recipyrc_file)
            if os.path.isfile(path):
                os.remove(path)

    def teardown_method(self, method):
        """
        py.test-compliant teardown function, run after each test method,
        deletes files in test_files.

        :param method: Test method
        :type method: function
        """
        if os.path.isfile(TestRecipyrc.test_output_data):
            os.remove(TestRecipyrc.test_output_data)

    def test_recipyrc(self):
        """
        Test that if neither .recipyrc, recipyrc nor ~/recipyrc exist then
        recipy uses its default configuration. As part of this test, a
        test is also done that a database is created at in
        ~/recipy/recipyDB.json.
        """
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        recipydb = get_recipydb()
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    @pytest.mark.parametrize("recipyrc", [
        get_recipyrc(),
        os.path.join(os.getcwd(), ".recipyrc"),
        os.path.join(os.getcwd(), "recipyrc")])
    def test_user_recipyrc(self, recipyrc):
        """
        Test that if ~/recipy/recipyrc, .recipy or recipyrc are present
        then their configuration is used. As part of this test, this
        also tests that that if [database] 'path' is valid then a
        database is created at that path.

        :param recipyrc: recipyrc file
        :type recipyrc: str or unicode
        """
        recipydb = os.path.join(TestRecipyrc.test_directory,
                                str(id(self)) + "DB.json")
        TestRecipyrc.update_recipyrc(recipyrc, "database", "path", recipydb)
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    @pytest.mark.parametrize("recipyrc_files", [
        (os.path.join(os.getcwd(), ".recipyrc"), get_recipyrc()),
        (os.path.join(os.getcwd(), "recipyrc"), get_recipyrc()),
        (os.path.join(os.getcwd(), "recipyrc"),
         os.path.join(os.getcwd(), ".recipyrc"))])
    def test_recipyrc_precedence(self, recipyrc_files):
        """
        Test the following scenarios:

        * If both .recipyrc and ~/recipy/recipyrc are present then the
          former's configuration is used.
        * If both recipyrc and ~/recipy/recipyrc are present then the
          former's configuration is used.
        * If both recipyrc and .recipyrc are present then the former's
          configuration is used.

        :param recipyrc_files: two recipyrc files, the former of which is
         expected to take precedence
        :type recipyrc_files: tuple of (str or unicode, str or unicode)
        """
        (recipyrc, ignore_recipyrc) = recipyrc_files
        recipydb = os.path.join(TestRecipyrc.test_directory,
                                str(id(self)) + "DB.json")
        TestRecipyrc.update_recipyrc(recipyrc,
                                     "database", "path", recipydb)
        ignore_recipydb = os.path.join(TestRecipyrc.test_directory,
                                str(id(self)) + "ignoreDB.json")
        TestRecipyrc.update_recipyrc(ignore_recipyrc,
                                     "database", "path", ignore_recipydb)
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)
        assert not os.path.isfile(ignore_recipydb),\
            ("Did not expect to find " + ignore_recipydb)

    def test_unknown_section(self):
        """
        Test that if ~/recipy/recipyrc has an unknown section then the
        section is ignored and the rest of the configuration is used
        successfully.
        """
        recipyrc = get_recipyrc()
        TestRecipyrc.update_recipyrc(recipyrc, "unknown", "unknown", "unknown")
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        recipydb = get_recipydb()
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    def test_unknown_parameter(self):
        """
        Test that if ~/recipy/recipyrc has an unknown parameter then
        the parameter is ignored and the rest of the configuration is
        used successfully.
        """
        recipyrc = get_recipyrc()
        recipydb = get_recipydb()
        TestRecipyrc.update_recipyrc(recipyrc,
                                     "database", "unknown", "unknown")
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    def test_unknown_database_path(self):
        """
        Test that if ~/recipy/recipyrc has a [database] 'path' that does
        not exist then recipy fails with exit code 1.
        """
        recipyrc = get_recipyrc()
        TestRecipyrc.update_recipyrc(recipyrc, "database", "path", "unknown")
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 1, ("Unexpected exit code " + exit_code)

    def test_general_debug(self):
        """
        Test that if ~/recipy/recipyrc has a [general] 'debug' entry 
        then debugging information is printed.
        """
        recipyrc = get_recipyrc()
        TestRecipyrc.update_recipyrc(recipyrc, "general", "debug")
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        # TODO capture stdout and pattern match.

    def test_general_quiet(self):
        """
        Test that if ~/recipy/recipyrc has a [general] 'quiet' entry 
        then no information is printed.
        """
        recipyrc = get_recipyrc()
        TestRecipyrc.update_recipyrc(recipyrc, "general", "quiet")
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        # TODO capture stdout and pattern match.

    @pytest.mark.parametrize("ignores", [
        ("input_hashes", "inputs"),
        ("output_hashes", "outputs")])
    def test_ignored_metadata_hashes(self, ignores):
        """
        Test that if ~/recipy/recipyrc has a [ignored metadata]
        'input_hashes' or 'output_hashes' entries then no hashes
        are recorded for input/output files.
        """
        (config_key, log_key) = ignores
        recipyrc = get_recipyrc()
        TestRecipyrc.update_recipyrc(recipyrc, "ignored metadata", config_key)
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        (log, _) = TestRecipyrc.get_log(get_recipydb())
        files = log[log_key]
        assert len(files) == 1, ("Unexpected number of files")
        assert type(files[0]) is not list, ("Unexpected list")

    def test_data_file_diff_outputs(self):
        """
        Test that if ~/recipy/recipyrc has a [data]
        'file_diff_outputs' entry then:

        * If a script is run that creates output files, then 
          no corresponding entry for that run in the 'filediffs' in
          the database.
        * If the script is rerun, then there will be a corresponding
          entry for that run in the 'filediffs' in the database, with
          an empty 'diffs' value.
        """
        recipyrc = get_recipyrc()
        TestRecipyrc.update_recipyrc(recipyrc, "data", "file_diff_outputs")
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        _, filediffs = TestRecipyrc.get_log(get_recipydb())
        assert filediffs is None, "Expected filediffs to be null"

        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        _, filediffs = TestRecipyrc.get_log(get_recipydb())
        assert filediffs is not None, ("Expected filediffs not to be null")
        assert filediffs["filename"] == TestRecipyrc.test_output_data,\
            ("Expected filediffs['filename'] to be " +
            TestRecipyrc.test_output_data)
        assert filediffs["diff"] == ""

    def test_data_file_diff_outputs_records_diff(self):
        """
        Test that if ~/recipy/recipyrc has a [data]
        'file_diff_outputs' entry then if a script is run that creates
        output files, and the output files already exist, and are
        changed, then there will be a corresponding entry for that run
        in the 'filediffs' in the database, with a 'diffs' value
        holding information on the difference.
        """
        recipyrc = get_recipyrc()
        TestRecipyrc.update_recipyrc(recipyrc, "data", "file_diff_outputs")
        # Create an empty output file.
        open(TestRecipyrc.test_output_data, 'w').close()
        exit_code = TestRecipyrc.run_script()
        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        _, filediffs = TestRecipyrc.get_log(get_recipydb())
        assert filediffs is not None, ("Expected filediffs not to be null")
        assert filediffs["filename"] == TestRecipyrc.test_output_data,\
            ("Expected filediffs['filename'] to be " +
            TestRecipyrc.test_output_data)
        assert "before this run" in filediffs["diff"],\
               "Expected filediffs['diffs'] to record 'before this run'"
        assert "after this run" in filediffs["diff"],\
               "Expected filediffs['diffs'] to record 'after this run'"
