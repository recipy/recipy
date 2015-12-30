import os, sys, subprocess
from tinydb import TinyDB, where


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
