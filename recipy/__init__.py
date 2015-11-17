# These two lines ARE needed, as they actually set up sys.meta_path
from . import PatchBaseScientific
from . import PatchScientific

from .log import *

__version__ = '0.2.3'

# Patch built-in open function
# orig_open = __builtins__['open']
# def patched_open(*args, **kwargs):
# 	print('Called open!')
# 	print(args)
# 	print(kwargs)
# 	return(orig_open(*args, **kwargs))

# __builtins__['open'] = patched_open

log_init()