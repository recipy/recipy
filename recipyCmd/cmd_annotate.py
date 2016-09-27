import os
import click
from tinydb import where
import tempfile
from recipyCommon.config import get_editor
from recipyCmd.templating import render_run_template
from recipyCmd.recipycmd import db, get_latest_run


@click.command('annotate', short_help='Add a note to the latest run.')
@click.option('--id', '-i', help='Tag run which id starts with TEXT.')
def cmd(id):
    """Add a note to the latest run using default text editor.
     You can also tag older runs using --id.

    \b
    For example: recipy tag -id 67d8
    Would add a note to run which id starts with 67d8"""
    editor = get_editor()

    if id:
        results = db.search(where('unique_id').matches('{}.*'.format(id)))
        if not results:
            click.echo('Could not find run starting with id {}'.format(id))
            return
        elif len(results) > 1:
            click.echo('Found more then one run with id {}'.format(id))
            return
        run = results[0]
    else:
        run = get_latest_run()

    # Get temp filename
    f = tempfile.NamedTemporaryFile(delete=False, mode='w')

    if run.get('notes'):
        f.write(run['notes'])

    # Write something to the bottom of it
    f.write('\n' + '-' * 80 + '\n')
    f.write('\n')
    f.write('Enter your notes on this run above this line')
    f.write('\n' * 3)
    f.write(render_run_template(run, nocolor=True))

    f.close()

    # Open your editor
    os.system('%s %s' % (editor, f.name))

    # Grab the text
    annotation = ""
    with open(f.name, 'r') as f:
        for line in f:
            if line == '-' * 80 + '\n':
                break
            annotation += line

    notes = annotation.strip()

    if notes == "":
        print('No annotation entered, exiting.')
        return

    # Store in the DB
    db.update({'notes': notes}, where('unique_id') == run['unique_id'])
    db.close()