from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from recipyGui import recipyGui
from recipyGui.models import Run
from forms import SearchForm

runs = Blueprint('runs', __name__, template_folder='templates')

@recipyGui.route('/')
def index():
    form = SearchForm()

    query = request.args.get('query', '')

    if not query:
        runs = Run.objects.all()
    else:
        # TODO: search runs using the query string
        runs = []

    print runs
    print query
    return render_template('runs/list.html', runs=runs, query=query, form=form)

#class ListView(MethodView):

#    def get(self):
#        runs = Run.objects.all()
#        print runs
#        return render_template('runs/list.html', runs=runs)

# Register urls
#runs.add_url_rule('/', view_func=ListView.as_view('list'))
