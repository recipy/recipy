from flask.ext.wtf import Form
from wtforms import StringField, SubmitField

class SearchForm(Form):
    query = StringField('query')
