from behave import given, when, then

import os

from behave_utils import setup_testing_environment


@given('we have recipy set up for testing')
def step_impl(context):
    context.db_file = setup_testing_environment("/Users/robin/code/recipy/test/scratch/")

@when('we run some code')
def step_impl(context):
    print(os.system("python example_script2.py"))

@then('an entry should be added to the database')
def step_impl(context):
    with open(context.db_file, 'r') as f:
    	contents = f.read()
    	assert "simple_test.npy" in contents