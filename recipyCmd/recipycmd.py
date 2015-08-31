#!/usr/bin/env python
"""recipy - a frictionless provenance tool for Python

Usage:
  recipy search [options] <outputfile>
  recipy latest [options]
  recipy gui [options]
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
  --debug       Turn on debugging mode

"""
import os
import re
import sys

from docopt import docopt
from pprint import pprint
from jinja2 import Template
from tinydb import TinyDB, where
from dateutil.parser import parse
import six

from . import __version__
from recipyCommon import config, utils


db = utils.open_or_create_db()


def print_result(r):
  # Print a single result from the search
    template = """Run ID: {{ unique_id }}
Created by {{ author }} on {{ date }}
Ran {{ script }} using {{ command }}
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

Outputs:
{% for output in outputs %}
  {{ output }}
{% endfor %}"""
    template = Template(template, trim_blocks=True)
    print(template.render(**r))


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

def gui(args):
  """
  Loads recipy GUI from the command-line
  """
  from recipyGui import recipyGui
  import threading, webbrowser, socket

  def get_free_port():
      s = socket.socket()
      s.bind(('', 0))
      port = s.getsockname()[1]
      s.close()
      return port

  port = get_free_port()
  url = "http://127.0.0.1:{0}".format(port)

  # Give the application some time before it starts
  threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

  # Turn off reloading by setting debug = False (this also fixes starting the
  # application twice)
  recipyGui.run(debug = args['--debug'], port=port)

def latest(args):
  results = db.all()

  results = [_change_date(result) for result in results]

  # Sort the results
  results = sorted(results, key = lambda x: parse(x['date']))

  print_result(results[-1])

  if args['--diff']:
    if 'diff' in results[-1]:
      print("\n\n")
      print(results[-1]['diff'])

  db.close()

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

  if len(results) == 0:
      print("No results found")
  else:
      if args['--all']:
          for r in results:
              print_result(r)
              print("-"*40)
      else:
          print_result(results[-1])
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
