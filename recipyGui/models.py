import datetime
from flask import url_for
from recipyGui import db

class Run(db.Document):
    title = db.StringField(max_length=255, required=True)
    filename = db.StringField(max_length=255, required=True)
    inputs = db.ListField(db.StringField(max_length=255))
    outputs = db.ListField(db.StringField(max_length=255))
    script = db.StringField(max_length=255, required=True)
    environment = db.ListField(db.StringField(max_length=255))
    command = db.StringField(max_length=255)
    gitrepo = db.StringField(max_length=255)
    gituser = db.StringField(max_length=30)
    gitcommit = db.StringField(max_length=255)
    date = db.DateTimeField(default=datetime.datetime.now, required=True)

    def get_absolute_url(self):
        return url_for('run', kwargs={title: self.title})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-date'],
        'ordering': ['-date']
    }
