import click


@click.command('annotate', short_help='Add a note to the latest run.')
@click.option('--id', '-i', help='Tag run which id starts with TEXT.')
def cmd(id):
    """Add a note to the latest run using default text editor.
     You can also tag older runs using --id.

    \b
    For example: recipy tag -id 67d8
    Would add a note to run which id starts with 67d8"""
    click.echo('Added Note...')
