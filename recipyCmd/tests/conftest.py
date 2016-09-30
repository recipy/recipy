import os
import pytest
from tinydb import TinyDB
from click.testing import CliRunner
from recipyCmd.recipycmd import CliConfig

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB = 'test.json'
DB_PATH = os.path.join(BASEDIR, TEST_DB)

test_runs_annotate = [
    {'date': u'{TinyDate}:2015-08-16T17:20:07',
     'unique_id': u'665b35e7',
     'notes': ''},
    {'date': u'{TinyDate}:2016-08-16T17:20:07',
     'unique_id': u'665a35e7',
     'notes': ''},
    {'date': u'{TinyDate}:2016-08-16T17:20:08',
     'unique_id': u'latest_run',
     'notes': ''},
    {'date': u'{TinyDate}:2016-08-16T17:20:07',
     'unique_id': u'765a35e7',
     'notes': 'original note'}
]


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def config():
    db = TinyDB(DB_PATH)
    for run in test_runs_annotate:
        db.insert(run)
    cfg = CliConfig()
    cfg.db = db
    yield cfg
    db.close()
    os.remove(DB_PATH)


@pytest.fixture()
def path_to_db():
    return DB_PATH
