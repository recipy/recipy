from flask import Blueprint, request, render_template
from recipyGui import recipyGui, db
from .forms import SearchForm
from tinydb import where
import re
from dateutil.parser import parse
import os

routes = Blueprint('routes', __name__, template_folder='templates')


@recipyGui.route('/')
def index():
    form = SearchForm()

    query = request.args.get('query', '')

    if not query:
        runs = db.all()
    else:
        # Search run outputs using the query string
        runs = db.search(where('outputs').any(lambda x: re.match(".+%s.+" % query, x)))
    runs = sorted(runs, key = lambda x: parse(x['date'].replace('{TinyDate}:', '')), reverse=True)

    return render_template('list.html', runs=runs, query=query, form=form)


@recipyGui.route('/run_details')
def run_details():
        form = SearchForm()
        query = request.args.get('query', '')
        run_id = int(request.args.get('id'))

        r = db.get(eid=run_id)

        return render_template('details.html', query=query, form=form, run=r)


@recipyGui.route('/latest_run')
def latest_run():
    form = SearchForm()

    runs = db.all()
    runs = sorted(runs, key = lambda x: parse(x['date'].replace('{TinyDate}:', '')), reverse=True)

    return render_template('details.html', query='', form=form, run=runs[0], active_page='latest_run')
