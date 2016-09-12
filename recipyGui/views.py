from flask import Blueprint, request, render_template, redirect, url_for, \
    escape, make_response, flash
from tinydb import Query, where
import os
from ast import literal_eval
from json import dumps

from recipyGui import recipyGui
from .forms import SearchForm, AnnotateRunForm

from recipyCommon.tinydb_utils import listsearch
from recipyCommon import utils
from recipyCmd.recipycmd import get_latest_run, _change_date


routes = Blueprint('routes', __name__, template_folder='templates')

if not os.path.exists(os.path.dirname(recipyGui.config.get('tinydb'))):
        os.mkdir(os.path.dirname(recipyGui.config.get('tinydb')))


@recipyGui.route('/')
def index():
    form = SearchForm()

    query = request.args.get('query', '').strip()

    db = utils.open_or_create_db()

    if not query:
        runs = db.all()
    else:
        # Search run outputs using the query string
        runs = db.search(
            where('outputs').any(lambda x: listsearch(query, x)) |
            where('inputs').any(lambda x: listsearch(query, x)) |
            where('script').search(query) |
            where('notes').search(query) |
            where('unique_id').search(query))

    runs = [_change_date(r) for r in runs]

    runs = sorted(runs, key=lambda x: x['date'], reverse=True)

    run_ids = []
    for run in runs:
        if 'notes' in run.keys():
            run['notes'] = str(escape(run['notes']))
        run_ids.append(run.eid)

    db.close()

    return render_template('list.html', runs=runs, query=query, form=form,
                           run_ids=str(run_ids),
                           dbfile=recipyGui.config.get('tinydb'))


@recipyGui.route('/run_details')
def run_details():
    form = SearchForm()
    annotateRunForm = AnnotateRunForm()
    query = request.args.get('query', '')
    run_id = int(request.args.get('id'))

    db = utils.open_or_create_db()
    r = db.get(eid=run_id)

    if r is not None:
        diffs = db.table('filediffs').search(Query().run_id == run_id)
    else:
        flash('Run not found.', 'danger')
        diffs = []

    r = _change_date(r)

    db.close()

    return render_template('details.html', query=query, form=form,
                           annotateRunForm=annotateRunForm, run=r,
                           dbfile=recipyGui.config.get('tinydb'), diffs=diffs)


@recipyGui.route('/latest_run')
def latest_run():
    form = SearchForm()
    annotateRunForm = AnnotateRunForm()

    db = utils.open_or_create_db()
    r = get_latest_run()

    if r is not None:
        diffs = db.table('filediffs').search(Query().run_id == r.eid)
    else:
        flash('No latest run (database is empty).', 'danger')
        diffs = []

    r = _change_date(r)

    db.close()

    return render_template('details.html', query='', form=form, run=r,
                           annotateRunForm=annotateRunForm,
                           dbfile=recipyGui.config.get('tinydb'), diffs=diffs,
                           active_page='latest_run')


@recipyGui.route('/annotate', methods=['POST'])
def annotate():
    notes = request.form['notes']
    run_id = int(request.form['run_id'])

    query = request.args.get('query', '')

    db = utils.open_or_create_db()
    db.update({'notes': notes}, eids=[run_id])
    db.close()

    return redirect(url_for('run_details', id=run_id, query=query))


@recipyGui.route('/runs2json', methods=['POST'])
def runs2json():
    run_ids = literal_eval(request.form['run_ids'])
    db = db = utils.open_or_create_db()
    runs = [db.get(eid=run_id) for run_id in run_ids]
    db.close()

    response = make_response(dumps(runs, indent=2, sort_keys=True))
    response.headers['content-type'] = 'application/json'
    response.headers['Content-Disposition'] = 'attachment; filename=runs.json'
    return response


@recipyGui.route('/patched_modules')
def patched_modules():
    db = utils.open_or_create_db()
    modules = db.table('patches').all()
    db.close()

    form = SearchForm()

    return render_template('patched_modules.html', form=form,
                           active_page='patched_modules', modules=modules,
                           dbfile=recipyGui.config.get('tinydb'))
