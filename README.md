# RecipyGui

A local webinterface to view and search runs stored by Recipy.

## Installation

RecipyGui is a Flask application. To install all requirements:

```pip install -r requirements.txt```

Make sure you have a MongoDB instance running with ```mongostat```, or else start it now:

```mongod```

## Usage

To start the local webserver, run:

```python recipy-gui.py```

You can find the gui at http://localhost:5000/
