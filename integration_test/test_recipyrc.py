import os
import os.path
from os.path import expanduser
import shutil
import tempfile

import pytest

from .database import open_db
from .process import execute

test_files = []

def get_home():
    return expanduser("~")
def get_recipy_dir():
    return os.path.expanduser("~/.recipy/")
def get_recipydb():
    return os.path.join(get_recipy_dir(), "recipyDB.json")
def get_recipyrc():
    return os.path.join(get_recipy_dir(), "recipyrc")
def run_script():
    execute("python", ["run_numpy.py"])

# TODO add to environment.py
# CONFIG.read(os.path.expanduser("~/.recipy/recipyrc"))
# return os.path.expanduser('~/.recipy/recipyDB.json')


def setup_function(function):
    """
    py.test-compliant setup function, run before each test function,
    deletes ~/.recipy.

    :param functon: Test function
    :type function: function
    """
    global test_files
    print("\nSETUP")
    print(type(function))
    recipy_dir = get_recipy_dir()
    if (os.path.isdir(recipy_dir)):
        shutil.rmtree(recipy_dir)
    os.mkdir(recipy_dir)
    test_files = []


def teardown_function(function):
    """
    py.test-compliant teardown function, run after each test function,
    deletes files in test_files.

    :param functon: Test function
    :type function: function
    """
    global test_files
    print("\nTEARDOWN")
    for test_file in test_files:
        if os.path.isfile(test_file):
            print("Removing", test_file)
            os.remove(test_file)


def test_default():
    """
    If neither .recipyrc, recipyrc nor ~/recipyrc exist then test that
    recipy uses its default configuration.
    """
    global test_files
    recipydb = get_recipydb()
    test_files.append(recipydb)
    run_script()
    assert os.path.isfile(recipydb), ("Expected to find " + recipydb)


def test_local_recipydb():
    """
    If ~/recipy/recipyrc is present. then test that its configuration
    is used.
    """
    global test_files
    recipydb =  os.path.join(os.getcwd(), "recipyDB.json")
    test_files.append(recipydb)
    recipyrc = get_recipyrc()
    with open(recipyrc, 'w') as f:
        f.write('[database]\n')
        f.write('path=' + recipydb + '\n')
    run_script()
    assert os.path.isfile(recipydb), ("Expected to find " + recipydb)


@pytest.mark.parametrize("config_file", [".recipyrc", "recipyrc"])
def test_local_recipyrc(config_file):
    """
    If .recipy or recipyrc are present. then test that their
    configuration is used.

    :param config_file: recipyrc file
    :type config_file: str or unicode
    """
    global test_files
    recipyrc = os.path.join(os.getcwd(), config_file)
    test_files.append(recipyrc)
    recipydb = os.path.join(os.getcwd(), "recipyDB.json")
    test_files.append(recipydb)
    with open(recipyrc, 'w') as f:
        f.write('[database]\n')
        f.write('path=' + recipydb + '\n')
    run_script()
    assert os.path.isfile(recipydb), ("Expected to find " + recipydb)
    assert len(os.listdir(get_recipy_dir())) == 0, "Expected .recipy to be empty"


@pytest.mark.parametrize("useit",[
     (".recipyrc", get_recipyrc()),
     ("recipyrc", get_recipyrc()),
     ("recipyrc", os.path.join(os.getcwd(), ".recipyrc"))
    ])
def test_local_recipyrc_precedence(useit):
    """
    Test the following scenarios:
    * If both .recipyrc and ~/recipy/recipyrc are present then the
      former's configuration is used.
    * If both recipyrc and ~/recipy/recipyrc are present then the
      former's configuration is used. 
    * If both recipyrc and .recipyrc are present then the former's
      configuration is used.  
    """
    global test_files
    (config_file, ignore_recipyrc) = useit

    recipyrc = os.path.join(os.getcwd(), config_file)
    test_files.append(recipyrc)
    recipydb = os.path.join(os.getcwd(), "recipyDB.json")
    test_files.append(recipydb)
    with open(recipyrc, 'w') as f:
        f.write('[database]\n')
        f.write('path=' + recipydb + '\n')

    test_files.append(ignore_recipyrc)
    ignore_recipydb = os.path.join(os.getcwd(), "ignoreDB.json")
    test_files.append(ignore_recipydb)
    with open(ignore_recipyrc, 'w') as f:
        f.write('[database]\n')
        f.write('path=' + ignore_recipydb + '\n')

    run_script()
    assert os.path.isfile(recipydb), ("Expected to find " + recipydb)
    assert not os.path.isfile(ignore_recipydb), ("Did not expect to find " + ignore_recipydb)


# import recipy
# import numpy as np
# data = np.array([list(range(4,8)), list(range(12,16))])
# np.savetxt("tmp.csv", data, delimiter=",")
# np.savetxt("tmp.txt", data, delimiter=",")
# np.loadtxt("tmp.csv", delimiter=",")
