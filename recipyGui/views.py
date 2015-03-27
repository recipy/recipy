from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from recipyGui import recipyGui
from recipyGui.models import Run
from flask import g

# Search functionality
from forms import SearchForm
@recipyGui.before_request
def before_request():
    g.search_form = SearchForm()

runs = Blueprint('runs', __name__, template_folder='templates')

@recipyGui.route('/', defaults = {'query': ''})
def index(query):
    runs = Run.objects.all()
    print runs
    print query
    return render_template('runs/list.html', runs=runs, query=query)

#class ListView(MethodView):

#    def get(self):
#        runs = Run.objects.all()
#        print runs
#        return render_template('runs/list.html', runs=runs)


@recipyGui.route('/search', methods=['POST'])
def search():
    #if not g.search_form.validate_on_submit():
    #    return redirect(url_for('index'))
    print g.search_form.search
    return redirect(url_for('index', query=g.search_form.search.data))

# Register urls
#runs.add_url_rule('/', view_func=ListView.as_view('list'))
