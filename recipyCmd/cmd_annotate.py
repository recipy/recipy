import click
from tinydb import where
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

    notes = get_message(run)

    if not notes:
        print('No notes added to run {}'.format(run['unique_id']))
        return

    db.update({'notes': notes}, where('unique_id') == run['unique_id'])
    db.close()


def get_message(run):
    """Gets message from user using default text editor."""
    notes = run.get('notes', '') + '\n'
    marker = '-' * 70
    instructions = 'Enter your notes above this line.\n'
    run_tmpl = render_run_template(run, nocolor=True)
    message = click.edit('\n'.join([notes, marker, instructions, run_tmpl]))
    if message is not None:
        return message.split(marker, 1)[0].rstrip('\n')
