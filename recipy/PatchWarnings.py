import warnings

from .log import log_warning

from recipyCommon.utils import reset_patches_table

warnings.showwarning = log_warning

# reset list of modules to be patched
reset_patches_table()
