import six

from .log import log_input, log_output


def open(*args, **kwargs):
    """Built-in open replacement that logs input and output

    Workaround for issue #44. Patching `__builtins__['open']` is complicated,
    because many libraries use standard open internally, while we only want to
    log inputs and outputs that are opened explicitly by the user.

    The user can either use `recipy.open` (only requires `import recipy` at the
    top of the script), or add `from recipy import open` and just use `open`.

    If python 2 is used, and an `encoding` parameter is passed to this
    function, `codecs` is used to open the file with proper encoding.
    """
    if six.PY3:
        mode = kwargs['mode']
        f = __builtins__['open'](*args, **kwargs)
    else:
        try:
            mode = args[1]
        except:
            mode = 'r'

        if 'encoding' in kwargs.keys():
            import codecs
            f = codecs.open(*args, **kwargs)
        else:
            f = __builtins__['open'](*args, **kwargs)

    # open file for reading?
    for c in 'r+':
        if c in mode:
            log_input(args[0], 'recipy.open')

    # open file for writing?
    for c in 'wax+':
        if c in mode:
            log_output(args[0], 'recipy.open')

    return(f)
