from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField


class SearchForm(FlaskForm):
    query = StringField('query')


class AnnotateRunForm(FlaskForm):
    notes = TextAreaField('notes')
    run_id = HiddenField('run_id')
