import wrapt
import os
import datetime
import sys
import getpass
import platform
import sys
from traceback import format_tb
from tinydb import TinyDB
import uuid

from git import Repo, InvalidGitRepositoryError

from recipyCommon.config import option_set
from recipyCommon.utils import open_or_create_db

RUN_ID = {}

def get_origin(repo):
    try:
        return repo.remotes.origin.url
    except:
        return None

def new_run():
    log_init()

def log_init():
    # Get the path of the script we're running
    # When running python -m recipy ..., during the recipy import argument 0
    # is -c (for Python 2) or -m (for Python 3) and the script is argument 1
    if sys.argv[0] in ['-c', '-m']:
        # Has the user called python -m recipy without further arguments?
        if len(sys.argv) < 2:
            return
        scriptpath = os.path.realpath(sys.argv[1])
        cmd_args = sys.argv[2:]
    else:
        scriptpath = os.path.realpath(sys.argv[0])
        cmd_args = sys.argv[1:]

    global RUN_ID

    # Open the database
    db = open_or_create_db()

    # Create the unique ID for this run
    guid = str(uuid.uuid4())
    
    
    
    # Get general metadata, environment info, etc
    run = {"unique_id": guid,
        "author": getpass.getuser(),
        "description": "",
        "inputs": [],
        "outputs": [],
        "script": scriptpath,
        "command": sys.executable,
        "environment": [platform.platform(), "python " + sys.version.split('\n')[0]],
        "date": datetime.datetime.utcnow(),
        "command_args": " ".join(cmd_args)}

    if not option_set('ignored metadata', 'git'):
        try:
            repo = Repo(scriptpath, search_parent_directories=True)
            run["gitrepo"] = repo.working_dir
            run["gitcommit"] =  repo.head.commit.hexsha
            run["gitorigin"] = get_origin(repo)

            if not option_set('ignored metadata', 'diff'):
                whole_diff = ''
                diffs = repo.index.diff(None, create_patch=True)
                for diff in diffs:
                    whole_diff += "\n\n\n" + diff.diff.decode("utf-8")

                run['diff'] = whole_diff
        except (InvalidGitRepositoryError, ValueError):
            # We can't store git info for some reason, so just skip it
            pass
    
    # Put basics into DB
    RUN_ID = db.insert(run)

    # Print message
    if not option_set('general', 'quiet'):
        print("recipy run inserted, with ID %s" % (guid))

    db.close()

    # Register exception hook so exceptions can be logged
    sys.excepthook = log_exception

def log_input(filename, source):
    if type(filename) is not str:
        try:
            filename = filename.name
        except:
            pass
    filename = os.path.abspath(filename)
    if option_set('general', 'debug'):
        print("Input from %s using %s" % (filename, source))
    #Update object in DB
    db = open_or_create_db()
    db.update(append("inputs", filename), eids=[RUN_ID])
    db.close()

def log_output(filename, source):
    if type(filename) is not str:
        try:
            filename = filename.name
        except:
            pass
    filename = os.path.abspath(filename)
    if option_set('general', 'debug'):
        print("Output to %s using %s" % (filename, source))
    #Update object in DB
    db = open_or_create_db()
    db.update(append("outputs", filename), eids=[RUN_ID])
    db.close()

def log_update(field, filename, source):
    filename = os.path.abspath(filename)
    print("Adding %s to %s using $s" % (field, filename, source))
    db = open_or_create_db()
    db.update(append(field, filename), eids=[RUN_ID])
    db.close()

def log_exception(typ, value, traceback):
    if option_set('general', 'debug'):
        print("Logging exception %s" % value)
    exception = {'type': typ.__name__,
                 'message': str(value),
                 'traceback': ''.join(format_tb(traceback))}
    # Update object in DB
    db = open_or_create_db()
    db.update({"exception": exception}, eids=[RUN_ID])
    db.close()
    # Done logging, call default exception handler
    sys.__excepthook__(typ, value, traceback)

def append(field, value):
    """
    Append a given value to a given array field.
    Keep an eye on https://github.com/msiemens/tinydb/issues/66
    """
    def transform(element):
        element[field].append(value)

    return transform


