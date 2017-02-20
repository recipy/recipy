from tinydb import where
from recipyCommon.tinydb_utils import listsearch


def search_database(db, query=None):
    """ Use this to perform a search of runs in the database """
    if not query:
        runs = db.all()
    else:
        # Search run outputs using the query string
        runs = db.search(
            where('outputs').any(lambda x: listsearch(query, x)) |
            where('inputs').any(lambda x: listsearch(query, x)) |
            where('script').search(query) |
            where('notes').search(query) |
            where('unique_id').search(query))
    return runs
