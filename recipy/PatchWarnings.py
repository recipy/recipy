import warnings

from .log import log_warning

from recipyCommon.utils import reset_patches_table


old_showwarning = warnings.showwarning


def showwarning(msg, typ, script, lineno, **kwargs):
    log_warning(msg, typ, script, lineno, **kwargs)

    # Done logging, print warning to stderr
    return old_showwarning(msg, typ, script, lineno)

warnings.showwarning = showwarning

# reset list of modules to be patched
reset_patches_table()
