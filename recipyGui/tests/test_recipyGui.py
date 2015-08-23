from recipyGui import recipyGui
from os import remove
from flask.ext.testing import TestCase
from tinydb import TinyDB


class TestRecipyGui(TestCase):
    def create_app(self):
        self.dbName = 'recipyGui/tests/test.json'
        recipyGui.config['tinydb'] = self.dbName
        recipyGui.config['TESTING'] = True

        self.db = TinyDB(self.dbName)

        return recipyGui

    def tearDown(self):
        self.db.close()
        remove(self.dbName)

    def test_index_view_empty_db(self):
        response = self.client.get('/')
        self.assert200(response)

        # needs blinker
        self.assert_template_used('list.html')
        self.assertContext('runs', [])
        self.assertContext('query', '')

    def test_index_view_db_with_run(self):
        run = {
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
        }
        self.db.insert(run)

        response = self.client.get('/')
        self.assert200(response)

        runs = self.get_context_variable('runs')

        for k, v in runs[0].iteritems():
            self.assertEqual(run.get(k), v)

    def test_index_view_run_with_nones(self):
        run = {
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
        }
        self.db.insert(run)

        response = self.client.get('/')
        self.assert200(response)

        runs = self.get_context_variable('runs')

        for k, v in runs[0].iteritems():
            self.assertEqual(run.get(k), v)

    def test_details_view_run_with_nones(self):
        run = {
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
        }
        eid = self.db.insert(run)

        response = self.client.get('/run_details?id={}'.format(eid))
        self.assert200(response)

        run2 = self.get_context_variable('run')

        for k, v in run2.iteritems():
            self.assertEqual(run.get(k), v)

        print run2
        self.assertEqual(True, False)
