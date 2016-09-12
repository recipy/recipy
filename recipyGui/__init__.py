from flask import Flask, url_for
from flask_bootstrap import Bootstrap
import re
from time import strptime, strftime
from os.path import abspath

from recipyCommon.config import get_db_path

recipyGui = Flask(__name__)
recipyGui.jinja_env.add_extension('jinja2.ext.do')
recipyGui.config['SECRET_KEY'] = 'geheim'
recipyGui.config['tinydb'] = abspath(get_db_path())

Bootstrap(recipyGui)

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
recipyGui.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename)
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
    if text is None:
        text = str(text)

    if query:
        replacement = r'<mark class="no-side-padding">\1</mark>'
        for q in query.split(' '):
            text = re.sub(r'(?i)({})'.format(q), replacement, text)
    return text

recipyGui.jinja_env.filters['highlight'] = highlight


@recipyGui.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    # TODO: this filter is currently not used. Can it be removed? Or do we want
    # a different date/time format in the gui?
    return value.strftime(format) + " UTC"

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
    if diff == '':
        return ''
    diff = diff.strip()
    diff = diff.replace('\n', '&nbsp;\n')
    diffData = diff.split('\n')
    openTag = '<tr><td class="'
    openTagEnd = '">'
    nbsp = '&nbsp;&nbsp;&nbsp;&nbsp;'
    data = '\n'.join([('%s%s%s%s<samp>%s</samp><td></tr>' %
                      (openTag,
                       'bg-info' if line.startswith('---') or line.startswith('+++')
                       else ('bg-danger' if line.startswith('-')
                             else ('bg-success' if line.startswith('+')
                                   else ('bg-info' if line.startswith('@')
                                         else ''))),
                       openTagEnd,
                       nbsp * line.count('\t'), line)) for line in diffData])
    return '<table width="100%">' + data + '</table>'

recipyGui.jinja_env.filters['colordiff'] = colordiff
