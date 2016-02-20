import os
import datetime
import sys
import getpass
import platform
import sys
import atexit
from traceback import format_tb
import uuid

from .version_control import add_git_info, hash_file
from recipyCommon.config import option_set
from recipyCommon.utils import open_or_create_db

RUN_ID = {}

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
        "exit_date": None,  # updated at script exit
        "command_args": " ".join(cmd_args)}

    if not option_set('ignored metadata', 'git'):
        add_git_info(run, scriptpath)

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
    if option_set('data', 'hash_inputs'):
        record = (filename, hash_file(filename))
    else:
        record = filename

    if option_set('general', 'debug'):
        print("Input from %s using %s" % (record, source))
    #Update object in DB
    db = open_or_create_db()
    db.update(append("inputs", record, no_duplicates=True), eids=[RUN_ID])
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
    # data hash will be hashed at script exit, if enabled
    db = open_or_create_db()
    db.update(append("outputs", filename, no_duplicates=True), eids=[RUN_ID])
    db.close()

def log_update(field, filename, source):
    filename = os.path.abspath(filename)
    print("Adding %s to %s using $s" % (field, filename, source))
    db = open_or_create_db()
    db.update(append(field, filename, no_duplicates=True), eids=[RUN_ID])
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

def append(field, value, no_duplicates=False):
    """
    Append a given value to a given array field.
    Keep an eye on https://github.com/msiemens/tinydb/issues/66
    """
    def transform(element):
        if no_duplicates and value in element[field]:
            pass
        else:
            element[field].append(value)

    return transform


# atexit functions will run on script exit (even on exception)
@atexit.register
def log_exit():
    # Update the record with the timestamp of the script's completion.
    # We don't save the duration because it's harder to serialize a timedelta.
    if option_set('general', 'debug'):
        print("recipy run complete")
    exit_date = datetime.datetime.utcnow()
    db = open_or_create_db()
    db.update({'exit_date': exit_date}, eids=[RUN_ID])
    db.close()

@atexit.register
def hash_outputs():
    # Writing to output files is complete; we can now compute hashes.
    if not option_set('data', 'hash_outputs'):
        return

    db = open_or_create_db()
    run = db.get(eid=RUN_ID)
    new_outputs = [(filename, hash_file(filename))
                   for filename in run.get('outputs')]
    db.update({'outputs': new_outputs}, eids=[RUN_ID])
    db.close()
