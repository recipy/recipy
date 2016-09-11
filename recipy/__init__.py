# These lines ARE needed, as they actually set up sys.meta_path
from . import PatchWarnings
from . import PatchBaseScientific
from . import PatchScientific

from .log import *

from .utils import open

__version__ = '0.2.3'

log_init()
