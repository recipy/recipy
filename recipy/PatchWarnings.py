import warnings

from .log import log_warning

from recipyCommon.utils import open_or_create_db

warnings.showwarning = log_warning

# reset list of modules to be patched
db = open_or_create_db()
patches = db.table('patches')
patches.purge()
patches.insert({'modules': []})
db.close()
