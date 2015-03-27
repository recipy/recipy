from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from recipyGui import recipyGui
from recipyGui.models import Run

runs = Blueprint('runs', __name__, template_folder='templates')

#@recipyGui.route('/')
#def index():
#    return render_template('index.html')

class ListView(MethodView):

    def get(self):
        runs = Run.objects.all()
        return render_template('runs/list.html', runs=runs)

# Register urls
runs.add_url_rule('/', view_func=ListView.as_view('list'))
