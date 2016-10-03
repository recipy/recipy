from json import dumps
import re
import os
import click
import six
from tinydb import Query

from recipyCommon.utils import json_serializer
from recipyCmd.recipycmd import pass_config
from recipyCmd.templating import render_run_template
from recipyCommon.version_control import hash_file


@click.command('search', short_help='Search for a run which generated the file.')
@click.option('--fuzzy', '-f', is_flag=True,
              help='Search based on part of FILE name or its path. Will accept Regex expressions.')
@click.option('--allruns', '-a', is_flag=True, help='Return all runs.')
@click.option('--diff', '-d', is_flag=True, help='Show diff. Ignored if --json.')
@click.option('--json', '-j', is_flag=True, help='Return results as JSON.')
@click.option('--inputs', is_flag=True, help='Restrict search to run inputs only.')
@click.option('--outputs', is_flag=True, help='Restrict search to run outputs only.')
@click.argument('file', required=True)
@pass_config
def cmd(config, fuzzy, allruns, diff, json, inputs, outputs, file):
    """Search for FILE among all inputs and outputs recorded by ReciPy and find the
    latest run which generated it. By default, it will search for hash of the FILE,
    you need to provide it with full name with extension.

    \b
    For example: recipy search -a --outputs newplot.pdf
    Will look through outputs of runs and return all runs
    which generated file with same hash as newplot.pdf

    \b
    recipy search -f plot.pdf
    Will look through inputs and outputs of runs and return
    latest run with file which had plot.pdf in its name."""

    db = config.db
    Run = Query()

    if fuzzy:
        results = db.search(Run.outputs.test(find_by_regex, '.*{}.*'.format(file)))
        results += db.search(Run.inputs.test(find_by_regex, '.*{}.*'.format(file)))
    else:
        try:
            assert os.path.isfile(file)
            hash_value = hash_file(file)
        except Exception:
            click.echo('No file {} found.'.format(file))
            return

        results = db.search(Run.outputs.test(find_by_hash, hash_value))
        results += db.search(Run.inputs.test(find_by_hash, hash_value))

    results.sort(key=lambda x: x['date'])

    if not results:
        click.echo('[]' if json else 'No runs found.')
        return

    if not allruns:
        # Return only the latest run
        if len(results) > 1:
            click.echo('***** Older runs found. Use -a --allruns to show. Below is most recent. *****')
        results = (results[-1], )

    if json:
        results_as_json = dumps(results, indent=2, sort_keys=True, default=json_serializer)
        click.echo(results_as_json)
        return
    else:
        separator = '-' * 60 + '\n'
        click.echo(separator.join((render_run_template(r) for r in results)))
        if diff and 'diff' in results[-1]:
            click.echo('\n\n' + results[-1]['diff'])


def find_by_hash(x, val):
    for output in x:
        if isinstance(output, six.string_types):
            # If it's just a string it doesn't have a hash
            # so skip it
            return False
        else:
            test_val = output[1]

        if test_val == val:
            return True


def find_by_regex(x, val):
    for output in x:
        if isinstance(output, six.string_types):
            test_val = output
        else:
            test_val = output[0]
        if re.match(val, test_val):
            return True
