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
  -h --help     Show this screen
  --version     Show version
  -a --all      Show all results (otherwise just latest result given)
  -f --fuzzy    Use fuzzy searching on filename
  -r --regex    Use regex searching on filename
  -i --id       Search based on (a fragment of) the run ID
  -v --verbose  Be verbose
  -d --diff     Show diff
  -j --json     Show output as JSON
  --no-browser  Do not open browser window
  --debug       Turn on debugging mode

"""
import os
import re
import sys
import tempfile

from docopt import docopt
from pprint import pprint
from jinja2 import Template
from tinydb import TinyDB, where
from dateutil.parser import parse
from json import dumps
import six

from . import __version__
from recipyCommon import config, utils


db = utils.open_or_create_db()


def template_result(r):
  # Print a single result from the search
    template = """Run ID: {{ unique_id }}
Created by {{ author }} on {{ date }} UTC
Ran {{ script }} using {{ command }}
{% if command_args|length > 0 %}
Using command-line arguments: {{ command_args }}
{% endif %}
{% if gitcommit is defined %}
Git: commit {{ gitcommit }}, in repo {{ gitrepo }}, with origin {{ gitorigin }}
{% endif %}
Environment: {{ environment|join(", ") }}
{% if exception is defined %}
Exception: ({{ exception.type }}) {{ exception.message }}
{% endif %}
{% if inputs|length == 0 %}
Inputs: none
{% else %}
Inputs:
{% for input in inputs %}
  {{ input }}
{% endfor %}
{% endif %}
{% if outputs | length == 0 %}
Outputs: none
{% else %}
Outputs:
{% for output in outputs %}
  {{ output }}
{% endfor %}
{% endif %}

{% if notes is defined %}
Notes:
{{ notes }}
{% endif %}
"""
    template = Template(template, trim_blocks=True)
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
  # Grab latest run from the DB
  run = get_latest_run()

  # Get temp filename
  f = tempfile.NamedTemporaryFile(delete=False, mode='w')

  # Write something to the bottom of it
  f.write('\n'+'-'*80+'\n')
  f.write('\n')
  f.write('Enter your notes on this run above this line')
  f.write('\n'*3)
  f.write(template_result(run))

  f.close()

  # Open your editor
  os.system('$EDITOR %s' % f.name)

  # Grab the text
  annotation = ""
  with open(f.name, 'r') as f:
    for line in f:
      if line == '-'*80+'\n':
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
  import threading, webbrowser, socket

  def get_free_port():
      port = None
      base_port = config.get_gui_port()
      for trial_port in range(base_port,base_port+5):
          try:
              s = socket.socket()
              s.bind(('', trial_port))
              s.close()
              port = trial_port
              break
          except OSError:
              # port already bound
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
      threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

  # Turn off reloading by setting debug = False (this also fixes starting the
  # application twice)
  recipyGui.run(debug = args['--debug'], port=port)

def get_latest_run():
  results = db.all()

  results = [_change_date(result) for result in results]

  # Sort the results
  results = sorted(results, key = lambda x: parse(x['date']))

  return results[-1]

def latest(args):

  run = get_latest_run()

  if args['--json']:
    output = dumps(run, indent=2, sort_keys=True)
    print(output)
  else:
    print(template_result(run))

    if args['--diff']:
      if 'diff' in run:
        print("\n\n")
        print(run['diff'])

def search(args):
  filename = args['<outputfile>']

  if args['--fuzzy']:
    results = db.search(where('outputs').any(lambda x: re.match(".+%s.+" % filename, x)))
  elif args['--regex']:
    results = db.search(where('outputs').any(lambda x: re.match(filename, x)))
  elif args['--id']:
    results = db.search(where('unique_id').matches('%s.+' % filename))
    # Automatically turn on display of all results so we don't misleadingly
    # suggest that their shortened ID is unique when it isn't
    args['--all'] = True
  else:
    results = db.search(where('outputs').any(os.path.abspath(filename)))

  results = [_change_date(result) for result in results]

  # Sort the results
  results = sorted(results, key = lambda x: parse(x['date']))

  if args['--json']:
    if args['--all']:
      res_to_output = results
    else:
      res_to_output = results[-1]
    output = dumps(res_to_output, indent=2, sort_keys=True)
    print(output)
  else:
    if len(results) == 0:
        print("No results found")
    else:
        if args['--all']:
            for r in results[:-1]:
                print(template_result(r))
                print("-"*40)
            print(template_result(results[-1]))
        else:
            print(template_result(results[-1]))
            if len(results) > 1:
                print("** Previous runs creating this output have been found. Run with --all to show. **")

            if args['--diff']:
              if 'diff' in results[-1]:
                print("\n\n")
                print(results[-1]['diff'])

  db.close()

def _change_date(result):
  result['date'] = result['date'].replace('{TinyDate}:', '')
  return result

if __name__ == '__main__':
  main()
