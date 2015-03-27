from flask import Flask, url_for
import os
from flask.ext.mongoengine import MongoEngine
from flask_bootstrap import Bootstrap

recipyGui = Flask(__name__)
Bootstrap(recipyGui)

# Determines the destination of the build. Only usefull if you're using Frozen-Flask
recipyGui.config['FREEZER_DESTINATION'] = os.path.dirname(os.path.abspath(__file__))+'/../build'

# MongoDB settings
recipyGui.config["MONGODB_SETTINGS"] = {'DB': "test_database"}
recipyGui.config["SECRET_KEY"] = "geheim"

db = MongoEngine(recipyGui)

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
recipyGui.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)

def register_blueprints(app):
    # Prevents circular imports
    from recipyGui.views import runs
    recipyGui.register_blueprint(runs)

register_blueprints(recipyGui)
