import wrapt

def recursive_getattr(obj, attr):
    prev_part = obj

    for part in attr.split("."):
        prev_part = getattr(prev_part, part)

    return prev_part

def recursive_setattr(obj, attr, value):
    prev_part = obj

    for part in attr.split(".")[:-1]:
        prev_part = getattr(prev_part, part)

    setattr(prev_part, attr.split(".")[-1], value)

def patch_function(mod, function, wrapper):
        old_f_name = '_%s' % function.replace(".", "_")
        setattr(mod, old_f_name, recursive_getattr(mod, function))

        recursive_setattr(mod, function, wrapper(getattr(mod, old_f_name)))

def create_wrapper(function, arg_loc, source):
    @wrapt.decorator
    def f(self, wrapped, instance, args, kwargs):
        function(args[arg_loc], source)
        return wrapped(*args, **kwargs)

    return f
