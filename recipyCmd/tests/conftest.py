import os
import pytest
from tinydb import TinyDB
from click.testing import CliRunner
from recipyCmd.recipycmd import CliConfig

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB = 'test.json'
DB_PATH = os.path.join(BASEDIR, TEST_DB)

test_runs_annotate = [
    {'diff': u'diff of earliest run',
     'date': u'{TinyDate}:2014-08-16T17:20:07',
     'unique_id': u'665b35e7',
     'notes': '',
     'inputs': [],
     'outputs': ['C:\\Code\\test-recipy\\early_plot.jpg']},
    {'date': u'{TinyDate}:2016-08-16T17:20:07',
     'unique_id': u'665a35e7',
     'notes': '',
     'inputs': [],
     'outputs': ['C:\\Code\\test-recipy\\best_plot.jpg']},
    {'diff': u'diff of latest run',
     'date': u'{TinyDate}:2016-08-16T17:20:08',
     'unique_id': u'latest_run',
     'notes': '',
     'inputs': ['input_file.csv', '/user/data/input_data.pdf'],
     'outputs': ['/user/data/output_table.svg', 'early_plot.jpg']},
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


@pytest.fixture
def config_empty_db():
    db = TinyDB(DB_PATH)
    cfg = CliConfig()
    cfg.db = db
    yield cfg
    db.close()
    os.remove(DB_PATH)


@pytest.fixture()
def path_to_db():
    return DB_PATH
