from flask import Flask, url_for
import os
from flask_bootstrap import Bootstrap
import re
from time import strptime, strftime

from recipyCommon.config import get_db_path

recipyGui = Flask(__name__)
recipyGui.config['SECRET_KEY'] = 'geheim'
recipyGui.config['tinydb'] = get_db_path()

Bootstrap(recipyGui)

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
recipyGui.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)

def register_blueprints(app):
    # Prevents circular imports
    from recipyGui.views import routes
    recipyGui.register_blueprint(routes)

register_blueprints(recipyGui)

# Custom filters
@recipyGui.template_filter()
def highlight(text, query=None):
    """Filter to highlight query terms in search results."""
    if query:
        replacement = r'<mark class="no-side-padding">\1</mark>'
        for q in query.split(' '):
            text = re.sub(r'(?i)({})'.format(q), replacement, text)
    return text

recipyGui.jinja_env.filters['highlight'] = highlight

@recipyGui.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    value = strptime(value, '{TinyDate}:%Y-%m-%dT%H:%M:%S')
    return strftime(format, value) + " UTC"

recipyGui.jinja_env.filters['datetimefilter'] = datetimefilter

@recipyGui.template_filter()
def gitorigin2url(origin):
    """convert a datetime to a different format."""
    url = origin.replace(':', '/')
    url = url.replace('git@', 'http://')
    url = url.replace('.git', '')

    return url

recipyGui.jinja_env.filters['gitorigin2url'] = gitorigin2url

@recipyGui.template_filter()
def colordiff(diff):
    """convert git diff data to html/bootstrap color code"""
    if diff=='':
        return ''
    diff = diff.strip()
    diff = diff.replace('\n', '&nbsp;\n')
    diffData = diff.split('\n')
    print(diffData)
    openTag = '<tr><td class="'
    openTagEnd = '">'
    nbsp = '&nbsp;&nbsp;&nbsp;&nbsp;'
    data = '\n'.join([('%s%s%s%s<samp>%s</samp><td></tr>' % (openTag, 'bg-danger' if line.startswith('-') else ('bg-success' if line.startswith('+') else ('bg-info' if line.startswith('@') else '')), openTagEnd, nbsp*line.count('\t') ,line)) for line in diffData])
    return '<table width="100%">'+data+'</table>'

recipyGui.jinja_env.filters['colordiff'] = colordiff
