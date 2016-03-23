import warnings

from .log import log_warning

warnings.showwarning = log_warning
