#!/usr/bin/env python
"""recipy - a frictionless provenance tool for Python

Usage:
  recipy search [options] <outputfile>
  recipy latest [options]
  recipy gui [options]
  recipy annotate [options]
  recipy (-h | --help)
  recipy --version

Options:
  -h --help        Show this screen
  --version        Show version
  -p --filepath    Search based on filepath rather than hash
  -f --fuzzy       Use fuzzy searching on filename
  -r --regex       Use regex searching on filename
  -i --id          Search based on (a fragment of) the run ID
  -a --all         Show all results (otherwise just latest result given)
  -v --verbose     Be verbose
  -d --diff        Show diff
  -j --json        Show output as JSON
  --no-browser     Do not open browser window
  --debug          Turn on debugging mode

"""
import os
import re
import tempfile

from docopt import docopt
from jinja2 import Template
from tinydb import where, Query
from json import dumps

import six

from . import __version__
from recipyCommon import config, utils
from recipyCommon.version_control import hash_file

from colorama import init
init()

db = utils.open_or_create_db()

template_str = """\aRun ID:\b {{ unique_id }}
\aCreated by\b {{ author }} on {{ date }} UTC
\aRan\b {{ script }} using {{ command }}
{% if command_args|length > 0 %}
Using command-line arguments: {{ command_args }}
{% endif %}
{% if gitcommit is defined %}
\aGit:\b commit {{ gitcommit }}, in repo {{ gitrepo }}, with origin {{ gitorigin }}
{% endif %}
\aEnvironment:\b {{ environment|join(", ") }}
{% if libraries is defined %}
\aLibraries:\b {{ libraries|join(", ") }}
{% endif %}
{% if exception is defined %}
\aException:\b ({{ exception.type }}) {{ exception.message }}
{% endif %}
{% if inputs|length == 0 %}
\aInputs:\b none
{% else %}
\aInputs:\b
{% for input in inputs %}
{% if input is string %}
{{ input }}
{% else %}
{{ input[0] }} ({{ input[1] }})
{% endif %}
{% endfor %}
{% endif %}
{% if outputs | length == 0 %}
\aOutputs:\b none
{% else %}
\aOutputs:\b
{% for output in outputs %}
{% if output is string %}
{{ output }}
{% else %}
{{ output[0] }} ({{ output[1] }})
{% endif %}
{% endfor %}
{% endif %}

{% if notes is defined %}
\aNotes:\b
{{ notes }}
{% endif %}
"""

BOLD = '\033[1m'
RESET = '\033[0m'

template_str_withcolor = template_str.replace('\a', BOLD).replace('\b', RESET)
template_str_nocolor = template_str.replace('\a', '').replace('\b', '')


def template_result(r, nocolor=False):
    # Print a single result from the search
    if nocolor:
        template_str = template_str_nocolor
    else:
        template_str = template_str_withcolor

    template = Template(template_str, trim_blocks=True)
    return template.render(**r)


def main():
    """
    Main function for recipy command-line script
    """
    args = docopt(__doc__, version='recipy v%s' % __version__)

    if args['--debug']:
        print('Command-line arguments: ')
        print(args)
        print('DB path: ', config.get_db_path())
        print('')
        print('Full config file (as interpreted):')
        print('----------------------------------')
        conf = config.read_config_file()
        s = six.StringIO()
        conf.write(s)
        print(s.getvalue())
        print('----------------------------------')

    if args['search']:
        search(args)
    elif args['latest']:
        latest(args)
    elif args['gui']:
        gui(args)
    elif args['annotate']:
        annotate(args)


def annotate(args):
    # check that $EDITOR is defined
    if os.environ.get('EDITOR') is None:
        print('No environment variable $EDITOR defined, exiting.')
        return

    # Grab latest run from the DB
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
    f.write(template_result(run, nocolor=True))

    f.close()

    # Open your editor
    os.system('$EDITOR %s' % f.name)

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


def gui(args):
    """
    Loads recipy GUI from the command-line
    """
    from recipyGui import recipyGui
    import threading
    import webbrowser
    import socket

    def get_free_port():
        port = None
        base_port = config.get_gui_port()
        for trial_port in range(base_port, base_port + 5):
            try:
                s = socket.socket()
                s.bind(('', trial_port))
                s.close()
                port = trial_port
                break
            except Exception:
                # port already bound
                # Please note that this also happens when the gui is run in
                # debug mode!
                pass
        if not port:
            # no free ports above, fall back to random
            s = socket.socket()
            s.bind(('', 0))
            port = s.getsockname()[1]
            s.close()
        return port

    port = get_free_port()
    url = "http://127.0.0.1:{0}".format(port)

    if not args['--no-browser']:
        # Give the application some time before it starts
        threading.Timer(1.25, lambda: webbrowser.open(url)).start()

    # Turn off reloading by setting debug = False (this also fixes starting the
    # application twice)
    recipyGui.run(debug=args['--debug'], port=port)


def get_latest_run():
    results = db.all()

    # If no runs in the database
    if len(results) == 0:
        return None

    results = [_change_date(result) for result in results]

    # Sort the results
    results = sorted(results, key=lambda x: x['date'])

    return results[-1]


def latest(args):
    run = get_latest_run()

    if not run:
        if args['--json']:
            print('[]')
            return
        else:
            print("Database is empty")
            return

    if args['--json']:
        output = dumps(run, indent=2, sort_keys=True, default=utils.json_serializer)
        print(output)
    else:
        print(template_result(run))

        if args['--diff']:
            if 'diff' in run:
                print("\n\n")
                print(run['diff'])


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


def find_by_filepath(x, val):
    for output in x:
        if isinstance(output, six.string_types):
            test_val = output
        else:
            test_val = output[0]
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


def search_hash(args):
    try:
        hash_value = hash_file(args['<outputfile>'])
    except Exception:
        # Probably an invalid filename/path so assume it is a raw hash value instead
        hash_value = args['<outputfile>']

    Run = Query()
    # Search both outputs AND inputs
    # TODO: Add a command-line argument to force searching of just one
    # of inputs or outputs
    results = db.search(Run.outputs.test(find_by_hash, hash_value))
    results += db.search(Run.inputs.test(find_by_hash, hash_value))

    results = sorted(results, key=lambda x: x['date'])

    if args['--json']:
        if len(results) == 0:
            print('[]')
            return
        if args['--all']:
            res_to_output = results
        else:
            res_to_output = results[-1]
        output = dumps(res_to_output, indent=2, sort_keys=True, default=utils.json_serializer)
        print(output)
    else:
        if len(results) == 0:
            print('No results found')
        else:
            if args['--all']:
                for r in results[:-1]:
                    print(template_result(r))
                    print("-" * 40)
                print(template_result(results[-1]))
            else:
                print(template_result(results[-1]))
                if len(results) > 1:
                    print("** Previous runs have been "
                          "found. Run with --all to show. **")

                if args['--diff']:
                    if 'diff' in results[-1]:
                        print("\n\n")
                        print(results[-1]['diff'])

    db.close()


def search(args):
    if args['--fuzzy'] or args['--id'] or args['--regex'] or args['--filepath']:
        search_text(args)
    else:
        search_hash(args)


def search_text(args):
    filename = args['<outputfile>']

    Run = Query()

    if args['--fuzzy']:
        results = db.search(Run.outputs.test(find_by_regex, ".+%s.+" % filename))
        results += db.search(Run.inputs.test(find_by_regex, ".+%s.+" % filename))
    elif args['--regex']:
        results = db.search(Run.outputs.test(find_by_regex, filename))
        results += db.search(Run.inputs.test(find_by_regex, filename))
    elif args['--id']:
        results = db.search(where('unique_id').matches('%s.*' % filename))
        # Automatically turn on display of all results so we don't misleadingly
        # suggest that their shortened ID is unique when it isn't
        args['--all'] = True
    elif args['--filepath']:
        results = db.search(Run.outputs.test(find_by_filepath, os.path.abspath(filename)))
        results += db.search(Run.inputs.test(find_by_filepath, os.path.abspath(filename)))
    else:
        print('Unknown arguments')
        print(__doc__)
        return

    # Sort the results
    results = sorted(results, key=lambda x: x['date'])

    if args['--json']:
        if len(results) == 0:
            print('[]')
            return
        if args['--all']:
            res_to_output = results
        else:
            res_to_output = results[-1]
        output = dumps(res_to_output, indent=2, sort_keys=True, default=utils.json_serializer)
        print(output)
    else:
        if len(results) == 0:
            print("No results found")
        else:
            if args['--all']:
                for r in results[:-1]:
                    print(template_result(r))
                    print("-" * 40)
                print(template_result(results[-1]))
            else:
                print(template_result(results[-1]))
                if len(results) > 1:
                    print("** Previous runs have been "
                          "found. Run with --all to show. **")

                if args['--diff']:
                    if 'diff' in results[-1]:
                        print("\n\n")
                        print(results[-1]['diff'])

    db.close()


def _change_date(result):
    result['date'] = str(result['date']).replace('{TinyDate}:', '')
    return result

if __name__ == '__main__':
    main()
