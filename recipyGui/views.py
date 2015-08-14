from flask import Blueprint, request, render_template
from recipyGui import recipyGui, db
from forms import SearchForm

routes = Blueprint('routes', __name__, template_folder='templates')


@recipyGui.route('/')
def index():
    form = SearchForm()

    query = request.args.get('query', '')

    if not query:
        # Return all runs, ordered by date (oldest run first)
        # TODO: find out iftinydb supports sorting by date
        runs = db.all()[::-1]
    else:
        # Search runs using the query string
        # TODO: fix search
        runs = []

    return render_template('list.html', runs=runs, query=query, form=form)


@recipyGui.route('/run_details')
def run_details():
        form = SearchForm()
        query = request.args.get('query', '')
        run_id = int(request.args.get('id'))

        r = db.get(eid=run_id)

        return render_template('details.html', query=query, form=form, run=r)
