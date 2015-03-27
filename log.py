import wrapt



def log_input(filename, source):
	print "Input from %s using %s" % (filename, source)

def log_output(filename, source):
	print "Output to %s using %s" % (filename, source)