from flask import Blueprint, request, render_template
from recipyGui import recipyGui
from forms import SearchForm
from bson.objectid import ObjectId

routes = Blueprint('routes', __name__, template_folder='templates')


@recipyGui.route('/')
def index():
    form = SearchForm()

    query = request.args.get('query', '')

    if not query:
        # Return all runs, ordered by date (oldest run first)
        #runs = [r for r in mongo.db.recipies.find({}).sort('date', -1)]
        runs =[]
    else:
        # Search runs using the query string
        #q = { '$text': { '$search': query} }
        #score = { 'score': { '$meta': 'textScore' } }
        #score_sort = [('score', {'$meta': 'textScore'})]
        #runs = [r for r in mongo.db.recipies.find(q, score).sort(score_sort)]
        runs = []

    return render_template('list.html', runs=runs, query=query, form=form)


@recipyGui.route('/run_details')
def run_details():
        form = SearchForm()
        query = request.args.get('query', '')
        run_id = request.args.get('id', '')

        q = { '_id': ObjectId(run_id) }
        #r = mongo.db.recipies.find_one(q)
        r = None

        return render_template('details.html', query=query, form=form, run=r)
