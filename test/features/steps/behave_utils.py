import os, shutil

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