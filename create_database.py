from recipyGui.models import *

r = Run(title='Pretty picture 1', filename='example_script1.py')
r.inputs = ["data.csv", "path_to_input2", "path_to_input3"]
r.outputs = ["path_to_output1"]
r.script = 'path_to_script'
r.environment = ["python3.2", "PyMongo2.8", "MAC OS 10.10.02"]
r.command = "script -f flag"
r.gitrepo = "git://otherhost.org/user/repo.git"
r.gituser = "robintw"
r.gitcommit = "c72a071351e5b48e70f2515dce309671c4103586"
r.save()

r = Run(title='Other data', filename='example_script2.py')
r.inputs = ["path_to_input1", "path_to_input2", "path_to_input3"]
r.outputs = ["path_to_output1"]
r.script = 'path_to_script'
r.environment = ["python3.2", "PyMongo2.8", "MAC OS 10.10.02"]
r.command = "script -f flag"
r.gitrepo = "git://otherhost.org/user/repo.git"
r.gituser = "jvdzwaan"
r.gitcommit = "c72a071351e5b48e70f2515dce309671c4103586"
r.save()
