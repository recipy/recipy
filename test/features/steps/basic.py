from behave import when, then

import os, sys
import subprocess

from behave_utils import check_id_exists_in_db, run_script_and_get_id


@when('we run some code')
def step_impl(context):
    context.run_id = run_script_and_get_id('examples/example_script2.py')

@when('we run some code as a module')
def step_impl(context):
    output = subprocess.check_output([sys.executable, '-m', 'recipy', 'examples/example_script3.py', 'test.npy'], env={'PYTHONPATH': os.path.abspath('../')}).decode('utf-8')
    context.run_id = output.replace('recipy run inserted, with ID', '').strip()

@then('an entry should be added to the database')
def step_impl(context):
    check_id_exists_in_db(context.run_id, context.db_file)
