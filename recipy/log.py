from pymongo import MongoClient
import wrapt
import os
import datetime

def log_init():
        #Start mongoDB client
        client = MongoClient()

        #Access database named 'test_database'
        db = client.recipyDB

        #Create images collection
        recipies = db.recipies

        # Get env info, etc
        run = {"author": "Robin",
            "description": "Baking cakes...",
            "inputs": [],
            "outputs": [],
            "script": "example_script.py",
            "command": "python example_script.py",
            "gitrepo": "https://github.com/recipy/recipy.git",
            "gitcommit": "6a8b3c06c9b5c66b1bb48ba0dd3928d8ef748f84",
            "gituser": "robintw",
            "environment": ["python3.2", "PyMongo2.8", "MAC OS 10.10.02"],
            "date": "datetime.datetime.utcnow()"}


        # Put basics into DB
        run_id = recipies.insert(run)
        print "Run recipy inserted %s" % (run_id)

        pass


def log_input(filename, source, run_id):
	print "Input from %s using %s" % (filename, source)
        #Update object in DB
        recipies.find_and_modify(query={'_id':run_id}, update={"$push": {'inputs': ["/path/to/new_input"]}}, upsert=False, full_response= True)

def log_output(filename, source):
	print "Output to %s using %s" % (filename, source)
