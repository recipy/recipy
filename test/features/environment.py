import os
import tempfile
import shutil


TESTING_CONFIG = """[database]
path = %s
"""

def before_scenario(context, scenario):
    # Create temporary directory to hold database
    context.tmpdir = tempfile.mkdtemp()
    context.db_file = os.path.join(context.tmpdir, 'DB.json')

    # Write testing configuration file to current directory
    with open('.recipyrc', 'w') as f:
        f.write(TESTING_CONFIG % context.db_file)

def after_scenario(context, scenario):
    # Remove temporary directory holding database
    shutil.rmtree(context.tmpdir)
