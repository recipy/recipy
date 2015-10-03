# These two lines ARE needed, as they actually set up sys.meta_path
from . import PatchBaseScientific
from . import PatchScientific

from .log import *

__version__ = '0.2.1'

log_init()