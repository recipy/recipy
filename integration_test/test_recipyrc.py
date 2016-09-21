"""
Tests of recipy configuration, provided via 'recipyrc' configuration files.
"""

import os
import os.path
import shutil
import tempfile
import pytest

from .process import execute
from .environment import get_recipy_dir, get_recipydb, get_recipyrc


class TestRecipyrc:
    """
    Tests of recipy configuration, provided via 'recipyrc'
    configuration files.
    """

    TEST_SCRIPT_NAME = "run_numpy.py"
    TEST_DATA_NAME = "run_numpy.dat"
    test_script = TEST_SCRIPT_NAME
    test_data = TEST_DATA_NAME

    @classmethod
    def run_script(cls):
        """
        Run test_script using Python.

        :return: exit code
        :rtype: int
        """
        return execute("python", [TestRecipyrc.test_script])

    @classmethod
    def append_recipyrc_database(cls, recipyrc, recipydb):
        """
        Append [database] path=recipydb configuration to recipyrc.

        :param recipyrc: recipyrc configuration file
        :type recipyrc: str or unicode
        :param recipydb: recipydb database file
        :type recipydb: str or unicode
        """
        with open(recipyrc, 'a') as f:
            f.write('[database]\n')
            f.write('path=' + recipydb + '\n')

    @classmethod
    def setup_class(cls):
        """
        py.test-compliant setup function, run when module is loaded,
        creates TMP/run_numpy.py.
        """
        TestRecipyrc.test_script =\
            os.path.join(tempfile.gettempdir(),
                         TestRecipyrc.TEST_SCRIPT_NAME)
        TestRecipyrc.test_data =\
            os.path.join(tempfile.gettempdir(),
                         TestRecipyrc.TEST_DATA_NAME)
        with open(TestRecipyrc.test_script, "w") as f:
            f.write("import recipy")
            f.write("\n")
            f.write("import numpy as np")
            f.write("\n")
            f.write("data = np.array([list(range(4,8))])")
            f.write("\n")
            f.write("np.savetxt(" +
                    str(TestRecipyrc.test_data).__repr__() +
                    ", data, delimiter=',')")
            f.write("\n")

    @classmethod
    def teardown_class(cls):
        """
        py.test-compliant setup function, run when module is completed,
        deletes TMP/run_numpy.py and TMP/run_numpy.dat.
        """
        if os.path.isfile(TestRecipyrc.test_script):
            os.remove(TestRecipyrc.test_script)
        if os.path.isfile(TestRecipyrc.test_data):
            os.remove(TestRecipyrc.test_data)

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
        self.test_files = []

    def teardown_method(self, method):
        """
        py.test-compliant teardown function, run after each test method,
        deletes files in test_files.

        :param method: Test method
        :type method: function
        """
        for test_file in self.test_files:
            if os.path.isfile(test_file):
                os.remove(test_file)

    def test_default(self):
        """
        Test that if neither .recipyrc, recipyrc nor ~/recipyrc exist then
        recipy uses its default configuration. As part of this test, a
        test is also done that a database is created at in
        ~/recipy/recipyDB.json.
        """
        recipydb = get_recipydb()
        self.test_files.append(recipydb)

        exit_code = TestRecipyrc.run_script()

        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    @pytest.mark.parametrize("recipyrc", [
        get_recipyrc(),
        os.path.join(os.getcwd(), ".recipyrc"),
        os.path.join(os.getcwd(), "recipyrc")])
    def test_local_recipyrc(self, recipyrc):
        """
        Test that if ~/recipy/recipyrc, .recipy or recipyrc are present
        then their configuration is used. As part of this test, this
        also tests that that if [database] path is valid then a
        database is created at that path.

        :param recipyrc: recipyrc file
        :type recipyrc: str or unicode
        """
        self.test_files.append(recipyrc)
        recipydb = os.path.join(os.getcwd(), "recipyDB.json")
        self.test_files.append(recipydb)
        TestRecipyrc.append_recipyrc_database(recipyrc, recipydb)

        exit_code = TestRecipyrc.run_script()

        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    @pytest.mark.parametrize("recipyrc_files", [
        (os.path.join(os.getcwd(), ".recipyrc"), get_recipyrc()),
        (os.path.join(os.getcwd(), "recipyrc"), get_recipyrc()),
        (os.path.join(os.getcwd(), "recipyrc"),
         os.path.join(os.getcwd(), ".recipyrc"))])
    def test_local_recipyrc_precedence(self, recipyrc_files):
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

        self.test_files.append(recipyrc)
        self.test_files.append(ignore_recipyrc)

        recipydb = os.path.join(os.getcwd(), "recipyDB.json")
        self.test_files.append(recipydb)
        TestRecipyrc.append_recipyrc_database(recipyrc, recipydb)

        ignore_recipydb = os.path.join(os.getcwd(), "ignoreDB.json")
        self.test_files.append(ignore_recipydb)
        TestRecipyrc.append_recipyrc_database(ignore_recipyrc, ignore_recipydb)

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
        self.test_files.append(recipyrc)
        recipydb = get_recipydb()
        self.test_files.append(recipydb)
        TestRecipyrc.append_recipyrc_database(recipyrc, recipydb)
        with open(recipyrc, 'a') as f:
            f.write('[unknown]\n')
            f.write('unknown=unknown\n')

        exit_code = TestRecipyrc.run_script()

        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    def test_unknown_parameter(self):
        """
        Test that if ~/recipy/recipyrc has an unknown parameter then
        the parameter is ignored and the rest of the configuration is
        used successfully.
        """
        recipyrc = get_recipyrc()
        self.test_files.append(recipyrc)
        recipydb = get_recipydb()
        self.test_files.append(recipydb)
        TestRecipyrc.append_recipyrc_database(recipyrc, recipydb)
        with open(recipyrc, 'a') as f:
            f.write('unknown=unknown\n')

        exit_code = TestRecipyrc.run_script()

        assert exit_code == 0, ("Unexpected exit code " + exit_code)
        assert os.path.isfile(recipydb), ("Expected to find " + recipydb)

    def test_unknown_database_path(self):
        """
        Test that if ~/recipy/recipyrc has a [database] path that does
        not exist then recipy fails with exit code 1.
        """
        recipyrc = get_recipyrc()
        self.test_files.append(recipyrc)
        TestRecipyrc.append_recipyrc_database(recipyrc, "unknown")

        exit_code = TestRecipyrc.run_script()

        assert exit_code == 1, ("Unexpected exit code " + exit_code)
