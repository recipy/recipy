import os, sys, shutil, subprocess
from tinydb import TinyDB, where

TESTING_CONFIG = """[database]
path = %s
"""

def setup_testing_environment(path):
    # Remove the dir if it exists already
    if os.path.exists(path):
        shutil.rmtree(path)

    # Make the directory first
    os.makedirs(path)

    db_file = os.path.join(path, 'DB.json')
    config_file_contents = TESTING_CONFIG % db_file

    # Write testing configuration file
    with open('/Users/robin/code/recipy/test/.recipyrc', 'w') as f:
        f.write(config_file_contents)

    return db_file

def get_record_from_db(id, dbfile):
    db = TinyDB(dbfile)

    res = db.search(where('unique_id') == id)

    return res

def check_id_exists_in_db(id, dbfile):
    res = get_record_from_db(id, dbfile)

    assert len(res) == 1

def run_script_and_get_id(script):
    output = subprocess.check_output([sys.executable, script], env={'PYTHONPATH': os.path.abspath('../')}).decode('utf-8')
    run_id = output.replace('recipy run inserted, with ID', '').strip()

    return run_id