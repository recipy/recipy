import os
import datetime
import sys
import getpass
import platform
import atexit
from traceback import format_tb
import uuid
import tempfile
import shutil
from tinydb import Query
import difflib

from recipyCommon.version_control import add_git_info, hash_file
from recipyCommon.config import option_set, get_db_path
from recipyCommon.utils import open_or_create_db

RUN_ID = {}


def new_run():
    """Just an alias for the log_init function"""
    log_init()


def log_init():
    """Do the initial logging for a new run.

    Works out what script has been run, creates a new unique run ID,
    and gets the basic metadata.

    This is called when running `import recipy`.
    """
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
    """Log input to the database.

    Called by patched functions that do some sort of input (reading from a file
    etc) with the filename and some sort of information about the source.

    Note: the source parameter is currently not stored in the database.
    """
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
    """Log output to the database.

    Called by patched functions that do some sort of output (writing to a file
    etc) with the filename and some sort of information about the source.

    Note: the source parameter is currently not stored in the database.
    """
    if type(filename) is not str:
        try:
            filename = filename.name
        except:
            pass
    filename = os.path.abspath(filename)

    if option_set('data', 'file_diff_outputs') and os.path.isfile(filename):
        tf = tempfile.NamedTemporaryFile(delete=False)
        db = open_or_create_db()
        shutil.copy2(filename, tf.name)
        add_file_diff_to_db(filename, tf.name, db_path=get_db_path())

    if option_set('general', 'debug'):
        print("Output to %s using %s" % (filename, source))
    #Update object in DB
    # data hash will be hashed at script exit, if enabled
    db = open_or_create_db()
    db.update(append("outputs", filename, no_duplicates=True), eids=[RUN_ID])
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


def add_file_diff_to_db(filename, tempfilename, db_path=get_db_path()):
    db = open_or_create_db(path=db_path)
    diffs = db.table('filediffs')
    diffs.insert({'run_id': RUN_ID,
                  'filename': filename,
                  'tempfilename': tempfilename})
    db.close()


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


@atexit.register
def output_file_diffs():
    # Writing to output files is complete; we can now compute file diffs.
    if not option_set('data', 'file_diff_outputs'):
        return

    db = open_or_create_db()
    diffs_table = db.table('filediffs')
    diffs = diffs_table.search(Query().run_id == RUN_ID)
    for item in diffs:
        diff = difflib.unified_diff(open(item['tempfilename']).readlines(),
                                    open(item['filename']).readlines(),
                                    fromfile='before this run',
                                    tofile='after this run')
        diffs_table.update({'diff': ''.join([l for l in diff])},
                           eids=[item.eid])

        # delete temporary file
        os.remove(item['tempfilename'])
    db.close()
