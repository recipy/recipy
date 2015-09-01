from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, HiddenField

class SearchForm(Form):
    query = StringField('query')

class AnnotateRunForm(Form):
    notes = TextAreaField('notes')
    run_id = HiddenField('run_id')
