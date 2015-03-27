from flask import render_template
from recipyGui import recipyGui

@recipyGui.route('/')
def index():
    return render_template('index.html')
