import click
from json import dumps
from recipyCommon.utils import get_run, json_serializer
from recipyCmd.recipycmd import pass_config
from recipyCmd.templating import render_run_template


@click.command('latest', short_help='Show latest run.')
@click.option('--diff', '-d', is_flag=True, help='Show diff. Ignored if --json.')
@click.option('--json', '-j', is_flag=True, help='Return results as JSON.')
@pass_config
def cmd(config, diff, json):
    """Show latest run saved by ReciPy."""
    with config.db as db:
        run = get_run(db, latest=True)

    if not run:
        click.echo('[]' if json else 'Database is empty.')
        return

    if json:
        latest_run_json = dumps(run, indent=2, sort_keys=True, default=json_serializer)
        click.echo(latest_run_json)
    else:
        click.echo(render_run_template(run) + (run.get('diff', '') if diff else ''))
