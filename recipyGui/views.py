from flask import Blueprint, request, render_template, redirect, url_for, \
    escape, make_response
from recipyGui import recipyGui
from .forms import SearchForm, AnnotateRunForm
from tinydb import TinyDB, where
import re
from dateutil.parser import parse
import os
from ast import literal_eval
from json import dumps


routes = Blueprint('routes', __name__, template_folder='templates')

if not os.path.exists(os.path.dirname(recipyGui.config.get('tinydb'))):
        os.mkdir(os.path.dirname(recipyGui.config.get('tinydb')))


@recipyGui.route('/')
def index():
    form = SearchForm()

    query = request.args.get('query', '').strip()

    db = TinyDB(recipyGui.config.get('tinydb'))

    if not query:
        runs = db.all()
    else:
        # Search run outputs using the query string
        runs = db.search(
            where('outputs').any(lambda x: re.match(".+%s.+" % query, x)) |
            where('notes').contains(query) |
            where('unique_id').contains(query))
    runs = sorted(runs, key = lambda x: parse(x['date'].replace('{TinyDate}:', '')) if x['date'] is not None else x['eid'], reverse=True)

    run_ids = []
    for run in runs:
        if 'notes' in run.keys():
            run['notes'] = str(escape(run['notes']))
        run_ids.append(run.eid)

    db.close()

    return render_template('list.html', runs=runs, query=query, form=form,
                           run_ids=str(run_ids))


@recipyGui.route('/run_details')
def run_details():
        form = SearchForm()
        annotateRunForm = AnnotateRunForm()
        query = request.args.get('query', '')
        run_id = int(request.args.get('id'))

        db = TinyDB(recipyGui.config.get('tinydb'))
        r = db.get(eid=run_id)

        db.close()

        return render_template('details.html', query=query, form=form,
                               annotateRunForm=annotateRunForm, run=r)


@recipyGui.route('/latest_run')
def latest_run():
    form = SearchForm()
    annotateRunForm = AnnotateRunForm()

    db = TinyDB(recipyGui.config.get('tinydb'))

    runs = db.all()
    runs = sorted(runs, key = lambda x: parse(x['date'].replace('{TinyDate}:', '')), reverse=True)

    db.close()

    return render_template('details.html', query='', form=form, run=runs[0],
                           annotateRunForm=annotateRunForm,
                           active_page='latest_run')

@recipyGui.route('/annotate', methods=['POST'])
def annotate():
    notes = request.form['notes']
    run_id = int(request.form['run_id'])

    query = request.args.get('query', '')

    db = TinyDB(recipyGui.config.get('tinydb'))
    db.update({'notes': notes}, eids=[run_id])
    db.close()

    return redirect(url_for('run_details', id=run_id, query=query))

@recipyGui.route('/runs2json', methods=['POST'])
def runs2json():
    run_ids = literal_eval(request.form['run_ids'])
    db = TinyDB(recipyGui.config.get('tinydb'))
    runs = [db.get(eid=run_id) for run_id in run_ids]
    db.close()

    response = make_response(dumps(runs, indent=2, sort_keys=True))
    response.headers['content-type'] = 'application/json'
    response.headers['Content-Disposition'] = 'attachment; filename=runs.json'
    return response
