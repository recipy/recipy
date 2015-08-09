from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from recipyGui import recipyGui, mongo
from forms import SearchForm
from bson.objectid import ObjectId

runs = Blueprint('runs', __name__, template_folder='templates')

@recipyGui.route('/')
def index():
    form = SearchForm()

    query = request.args.get('query', '')

    if not query:
        # Return all runs, ordered by date (oldest run first)
        runs = [r for r in mongo.db.recipies.find({}).sort('date', -1)]
    else:
        # Search runs using the query string
        q = { '$text': { '$search': query} }
        score = { 'score': { '$meta': 'textScore' } }
        score_sort = [('score', {'$meta': 'textScore'})]
        runs = [r for r in mongo.db.recipies.find(q, score).sort(score_sort)]

    print 'runs:', runs
    print 'query:', query
    return render_template('runs/list.html', runs=runs, query=query, form=form)


@recipyGui.route('/run_details')
def run_details():
        form = SearchForm()
        query = request.args.get('query', '')
        run_id = request.args.get('id', '')

        q = { '_id': ObjectId(run_id) }
        r = mongo.db.recipies.find_one(q)
        print run_id
        print r

        return render_template('runs/details.html', query=query, form=form,
                               run=r)

#class ListView(MethodView):

#    def get(self):
#        runs = Run.objects.all()
#        print runs
#        return render_template('runs/list.html', runs=runs)

# Register urls
#runs.add_url_rule('/', view_func=ListView.as_view('list'))
