#!/usr/bin/env python
"""recipy - a frictionless provenance tool for Python

Usage:
  recipy search [options] <outputfile>
  recipy gui [options]
  recipy (-h | --help)
  recipy --version

Options:
  -h --help     Show this screen
  --version     Show version
  -a --all      Show all results (otherwise just latest result given)
  -f --fuzzy    Use fuzzy searching on filename
  -r --regex    Use regex searching on filename
  -v --verbose  Be verbose
  -d --diff     Show diff
  --debug       Turn on debugging mode

"""
import os
import re
from docopt import docopt
from tinydb import TinyDB, where
import sys
from pprint import pprint
from jinja2 import Template
from dateutil.parser import parse
from . import __version__

DBFILE = os.path.expanduser('~/.recipy/recipyDB.json')



def print_result(r):
  # Print a single result from the search
    template = """Run ID: {{ unique_id }}
Created by {{ author }} on {{ date }}
Ran {{ script }} using {{ command }}
{% if gitcommit is defined %}
Git: commit {{ gitcommit }}, in repo {{ gitrepo }}, with origin {{ gitorigin }}
{% endif %}
Environment: {{ environment|join(", ") }}
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
  args = docopt(__doc__, version='recipy v%s' % __version__)
  
  if args['--debug']:
      print(args)

  if args['search']:
    search(args)
  elif args['gui']:
    gui(args)

def gui(args):
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


def search(args):
  if not os.path.exists(os.path.dirname(DBFILE)):
      os.mkdir(os.path.dirname(DBFILE))

  db = TinyDB(DBFILE) 

  filename = args['<outputfile>']

  if args['--fuzzy']:
    results = db.search(where('outputs').any(lambda x: re.match(".+%s.+" % filename, x)))
  elif args['--regex']:
    results = db.search(where('outputs').any(lambda x: re.match(filename, x)))
  else:
    results = db.search(where('outputs').any(os.path.abspath(filename)))

  def change_date(result):
    result['date'] = result['date'].replace('{TinyDate}:', '')
    return result

  results = [change_date(result) for result in results]

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



if __name__ == '__main__':
  main()