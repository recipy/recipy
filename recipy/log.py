from pymongo import MongoClient
import wrapt
import os
import datetime
import sys
import getpass
import platform
import sys

RUN_ID = {}

def log_init():
    global RUN_ID
    #Start mongoDB client
    client = MongoClient()

    #Access database named 'test_database'
    db = client.recipyDB

    #Create images collection
    recipies = db.recipies

    # Get env info, etc
    run = {"author": getpass.getuser(),
        "description": "",
        "inputs": [],
        "outputs": [],
        "script": " ".join(sys.argv),
        "command": " ".join(sys.argv),
        "gitrepo": "https://github.com/recipy/recipy.git",
        "gitcommit": "6a8b3c06c9b5c66b1bb48ba0dd3928d8ef748f84",
        "gituser": "robintw",
        "environment": [platform.platform(), "python " + sys.version.split('\n')[0]],
        "date": datetime.datetime.utcnow()}


    # Put basics into DB
    RUN_ID = recipies.insert(run)
    print "Run recipy inserted %s" % (RUN_ID)
    client.close()

def log_input(filename, source):
    print "Input from %s using %s" % (filename, source)
    #Update object in DB

    client = MongoClient()

    #Access database named 'test_database'
    db = client.recipyDB

    #Create images collection
    recipies = db.recipies
    recipies.find_and_modify(query={'_id':RUN_ID}, update={"$push": {'inputs': filename}}, upsert=False, full_response=True)
    client.close()

def log_output(filename, source):
    print "Output to %s using %s" % (filename, source)
    client = MongoClient()

    #Access database named 'test_database'
    db = client.recipyDB

    #Create images collection
    recipies = db.recipies
    recipies.find_and_modify(query={'_id':RUN_ID}, update={"$push": {'outputs': filename}}, upsert=False, full_response=True)
    client.close()