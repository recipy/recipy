from behave import given, when, then

import os, sys
import subprocess
from datetime import datetime

from behave_utils import get_record_from_db, run_script_and_get_id


@given('the user opted in to hash data')
def step_impl(context):
    with open('.recipyrc', 'a') as f:
        f.write("[data]\nhash_inputs = true\nhash_outputs = true")

@when('we run some code')
def step_impl(context):
    context.run_id = run_script_and_get_id('examples/example_script2.py')

@when('we run some code as a module')
def step_impl(context):
    output = subprocess.check_output([sys.executable, '-m', 'recipy', 'examples/example_script3.py', 'test.npy'], env={'PYTHONPATH': os.path.abspath('../')}).decode('utf-8')
    context.run_id = output.replace('recipy run inserted, with ID', '').strip()

@then('an entry should be added to the database')
def step_impl(context):
    res = get_record_from_db(context.run_id, context.db_file)
    assert len(res) == 1

@then('it should have a recorded exit date')
def step_impl(context):
    run = get_record_from_db(context.run_id, context.db_file)[0]
    assert type(run.get('exit_date')) is datetime

@then('each output should have a SHA-1 hash')
def step_impl(context):
    run = get_record_from_db(context.run_id, context.db_file)[0]
    for filename, sha1 in run.get('outputs'):
        assert len(sha1) == 40
