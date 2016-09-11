from recipyGui import recipyGui
from os import remove
from flask_testing import TestCase
from tinydb import TinyDB
from dateutil.parser import parse

import six


class TestRecipyGui(TestCase):
    def create_app(self):
        self.dbName = 'recipyGui/tests/test.json'
        recipyGui.config['tinydb'] = self.dbName
        recipyGui.config['TESTING'] = True

        self.db = TinyDB(self.dbName)

        self.testRuns = [
            # working run (nothing wrong with it)
            {
                u'inputs': [],
                u'description': u'',
                u'script': u'/Users/janneke/Documents/code/recipy/example_script2.py',
                u'outputs': [u'/Users/janneke/Documents/code/recipy/testNGCM_2.npy'],
                u'author': u'janneke',
                u'gitorigin': u'git@github.com:recipy/recipy.git',
                u'environment': [u'Darwin-13.4.0-x86_64-i386-64bit', u'python 2.7.10 |Anaconda 2.1.0 (x86_64)| (default, May 28 2015, 17:04:42) '],
                u'gitrepo': u'/Users/janneke/Documents/code/recipy',
                u'command': u'/Users/janneke/anaconda/bin/python',
                u'gitcommit': u'a2d8a6a19f33c618943cc7876b5be11fbfe4583b',
                u'date': u'{TinyDate}:2015-08-16T17:20:07',
                u'diff': u"\n\n\n--- a/example_script.py\n+++ b/example_script.py\n@@ -7,5 +7,12 @@ data = pd.read_csv('data.csv')\n data.plot(x='year', y='temperature')\n savefig('newplot.pdf')\n \n+# adding some lines\n+# to test the difff\n+\n data.temperature = data.temperature * 100\n-data.to_csv('output2.csv')\n\\ No newline at end of file\n+data.to_csv('output2.csv')\n+\n+data.to_csv('output3.csv')\n+\n+# more added lines\n\n\n\n--- a/example_script2.py\n+++ b/example_script2.py\n@@ -6,3 +6,5 @@ arr = arr + 500\n # We've made a fairly big change here!\n \n numpy.save('testNGCM_2.npy', arr)\n+\n+# also adding lins to second file\n",
                u'unique_id': u'665a35e7-33eb-4c01-9f78-3560fd31546e'
            },
            # 'empty' run
            {
                u'inputs': [],
                u'description': None,
                u'script': None,
                u'outputs': [],
                u'author': None,
                u'gitorigin': None,
                u'environment': [],
                u'gitrepo': None,
                u'command': None,
                u'gitcommit': None,
                u'date': u'{TinyDate}:2015-08-16T17:20:07',
                u'diff': None,
                u'unique_id': None
            },
            # Run details that caused issue #42
            {
                'author': 'Robin',
                'command': 'C:\\Anaconda3\\python.exe',
                'date': '{TinyDate}:2015-08-22T08:42:59',
                'description': '',
                'diff': '',
                'environment': ['Windows-7-6.1.7601-SP1', 'python 3.4.3 |Anaconda 2.2.0 (64-bit)| (default, Mar  6 2015, 12:06:10) [MSC v.1600 64 bit (AMD64)]'],
                'gitcommit': 'c681315966a9fca0662f57ac45191eb9fdc8cd9c',
                'gitorigin': None,
                'gitrepo': 'C:\\Code\\test-recipy',
                'inputs': [],
                'outputs': ['C:\\Code\\test-recipy\\testNGCM_2.npy'],
                'script': 'C:\\Code\\test-recipy\\example_script2.py',
                'unique_id': '6daab87a-8cf2-4e3d-afb9-1ee5b6b8ecdb'
            },
            # No git info except for the commit (not sure this can happen)
            {
                'author': 'Robin',
                'command': 'C:\\Anaconda3\\python.exe',
                'date': '{TinyDate}:2015-08-22T08:42:59',
                'description': '',
                'diff': None,
                'environment': ['Windows-7-6.1.7601-SP1', 'python 3.4.3 |Anaconda 2.2.0 (64-bit)| (default, Mar  6 2015, 12:06:10) [MSC v.1600 64 bit (AMD64)]'],
                'gitcommit': 'c681315966a9fca0662f57ac45191eb9fdc8cd9c',
                'gitorigin': None,
                'gitrepo': None,
                'inputs': [],
                'outputs': ['C:\\Code\\test-recipy\\testNGCM_2.npy'],
                'script': 'C:\\Code\\test-recipy\\example_script2.py',
                'unique_id': '6daab87a-8cf2-4e3d-afb9-1ee5b6b8ecdb'
            },
            # Run with warnings
            {
                "author": "jvdzwaan",
                "command": "/home/jvdzwaan/.virtualenvs/recipy/bin/python",
                "command_args": "",
                "date": "{TinyDate}:2016-03-23T13:56:30",
                "description": "",
                "diff": "\n\n\n--- a/.recipyrc\n+++ /dev/null\n@@ -1,2 +0,0 @@\n-[database]\n-path = /home/jvdzwaan/data/tmp/recipy-demo.json\n\n\n\n--- a/example_script.py\n+++ b/example_script.py\n@@ -1,11 +1,33 @@\n-import recipy\n+import warnings\n+#warnings.showwarning = log_warning\n+\n+import sys\n import pandas as pd\n-from matplotlib.pyplot import *\n+#print sys.modules.keys()\n+print 'pandas' in sys.modules.keys()\n+\n+import recipy\n+\n+import numpy as np\n+#print sys.modules.keys()\n+\n+warnings.warn('tes warning in script')\n+\n+# importing\n+#import pandas as pd\n+#from matplotlib.pyplot import *\n+\n+#import sys\n+#del sys.modules['codecs']\n+#import codecs\n+\n+#import pandas as pd\n+#from matplotlib.pyplot import *\n \n data = pd.read_csv('data.csv')\n \n-data.plot(x='year', y='temperature')\n-savefig('newplot.pdf')\n+#data.plot(x='year', y='temperature')\n+#savefig('newplot.pdf')\n \n-data.temperature = data.temperature * 100.0\n+data.temperature = data.temperature * 150.0\n data.to_csv('output2.csv')\n",
                "environment": ["Linux-3.19.0-56-generic-x86_64-with-Ubuntu-14.04-trusty", "python 2.7.6 (default, Jun 22 2015, 17:58:13) "],
                "gitcommit": "c753b702e2a8ec79b6a5b055c9a4005c8e2f3cd8",
                "gitorigin": None,
                "gitrepo": "/home/jvdzwaan/code/recipy-demo",
                "inputs": [],
                "outputs": [],
                "script": "/home/jvdzwaan/code/recipy-demo/example_script.py",
                "unique_id": "5958ac06-1beb-45e6-8223-1a02b058e026",
                "warnings": [
                    {
                        "lineno": 9,
                        "message": "unable to patch module; recipy was imported after numpy",
                        "script": "example_script.py",
                        "type": "UserWarning"
                    },
                    {
                        "lineno": 9,
                        "message": "unable to patch module; recipy was imported after pandas",
                        "script": "example_script.py",
                        "type": "UserWarning"
                    },
                    {
                        "lineno": 14,
                        "message": "tes warning in script",
                        "script": "example_script.py",
                        "type": "UserWarning"
                    }
                ]
            },
            # Run with empty warnings
            {
                "author": "jvdzwaan",
                "command": "/home/jvdzwaan/.virtualenvs/recipy/bin/python",
                "command_args": "",
                "date": "{TinyDate}:2016-03-23T13:56:30",
                "description": "",
                "diff": "\n\n\n--- a/.recipyrc\n+++ /dev/null\n@@ -1,2 +0,0 @@\n-[database]\n-path = /home/jvdzwaan/data/tmp/recipy-demo.json\n\n\n\n--- a/example_script.py\n+++ b/example_script.py\n@@ -1,11 +1,33 @@\n-import recipy\n+import warnings\n+#warnings.showwarning = log_warning\n+\n+import sys\n import pandas as pd\n-from matplotlib.pyplot import *\n+#print sys.modules.keys()\n+print 'pandas' in sys.modules.keys()\n+\n+import recipy\n+\n+import numpy as np\n+#print sys.modules.keys()\n+\n+warnings.warn('tes warning in script')\n+\n+# importing\n+#import pandas as pd\n+#from matplotlib.pyplot import *\n+\n+#import sys\n+#del sys.modules['codecs']\n+#import codecs\n+\n+#import pandas as pd\n+#from matplotlib.pyplot import *\n \n data = pd.read_csv('data.csv')\n \n-data.plot(x='year', y='temperature')\n-savefig('newplot.pdf')\n+#data.plot(x='year', y='temperature')\n+#savefig('newplot.pdf')\n \n-data.temperature = data.temperature * 100.0\n+data.temperature = data.temperature * 150.0\n data.to_csv('output2.csv')\n",
                "environment": ["Linux-3.19.0-56-generic-x86_64-with-Ubuntu-14.04-trusty", "python 2.7.6 (default, Jun 22 2015, 17:58:13) "],
                "gitcommit": "c753b702e2a8ec79b6a5b055c9a4005c8e2f3cd8",
                "gitorigin": None,
                "gitrepo": "/home/jvdzwaan/code/recipy-demo",
                "inputs": [],
                "outputs": [],
                "script": "/home/jvdzwaan/code/recipy-demo/example_script.py",
                "unique_id": "5958ac06-1beb-45e6-8223-1a02b058e026",
                "warnings": []
            }
        ]

        return recipyGui

    def tearDown(self):
        self.db.close()
        remove(self.dbName)

    def test_index_view_empty_db(self):
        response = self.client.get('/')
        self.assert200(response)

        self.assert_template_used('list.html')
        self.assertContext('runs', [])
        self.assertContext('query', '')

    def test_index_view_db_with_run(self):
        run = self.testRuns[0]
        self.db.insert(run)

        response = self.client.get('/')
        self.assert200(response)

        runs = self.get_context_variable('runs')

        for k, v in six.iteritems(runs[0]):
            self.assertEqual(run.get(k), v)

    def test_index_view_test_runs(self):
        self.testRuns = sorted(self.testRuns, key = lambda x: parse(x['date'].replace('{TinyDate}:', '')) if x['date'] is not None else x['eid'], reverse=True)
        for run in self.testRuns:
            self.db.insert(run)

        response = self.client.get('/')
        self.assert200(response)

        runs = self.get_context_variable('runs')
        self.assertEqual(runs, self.testRuns)

    def test_details_view(self):
        for run in self.testRuns:
            eid = self.db.insert(run)

            response = self.client.get('/run_details?id={}'.format(eid))
            self.assert200(response)

            run2 = self.get_context_variable('run')

            for k, v in six.iteritems(run2):
                self.assertEqual(run.get(k), v)

    def test_dbfile_is_set_in_views(self):
        """The database file should be displayed in the index, and run_details
        views.
        """
        eid = self.db.insert(self.testRuns[0])

        views = ['/', '/run_details?id={}'.format(eid)]

        for v in views:
            response = self.client.get(v)
            dbfile2 = self.get_context_variable('dbfile')
            # is the right value set?
            self.assertEqual(recipyGui.config.get('tinydb'), dbfile2)
            # is the value displayed?
            assert recipyGui.config.get('tinydb') in response.data

    def test_display_warnings_in_views(self):
        """If the run contains warnings, they must be displayed in the index
        and run_details view.
        """
        for run in self.testRuns:
            eid = self.db.insert(run)
            response = self.client.get('/run_details?id={}'.format(eid))
            if 'warnings' in run.keys():
                if run['warnings'] != []:
                    for w in run['warnings']:
                        assert w['message'] in response.data
                else:
                    assert 'Warnings' not in response.data
            else:
                assert 'Warnings' not in response.data
