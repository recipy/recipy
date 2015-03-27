from wrapt import wrap_function_wrapper
def _mkdtemp_wrapper(wrapped, instance, args, kwargs):
    print 'calling', wrapped.__name__
    return wrapped(*args, **kwargs)
def apply_patch(module):
    print 'patching', module.__name__
    wrap_function_wrapper(module, 'mkdtemp', _mkdtemp_wrapper)