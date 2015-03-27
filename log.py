import wrapt


@wrapt.decorator
def log_input(wrapped, instance, args, kwargs):
    print "Logging input"
    print args
    return wrapped(*args, **kwargs)
 
@wrapt.decorator
def log_output(wrapped, instance, args, kwargs):
    print "Logging output"
    print args
    return wrapped(*args, **kwargs)