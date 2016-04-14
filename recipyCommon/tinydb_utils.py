import six
import re
from datetime import datetime

from tinydb_serialization import Serializer, SerializationMiddleware


class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles
    FORMAT = '%Y-%m-%dT%H:%M:%S'

    def encode(self, obj):
        return obj.strftime(self.FORMAT)

    def decode(self, s):
        return datetime.strptime(s, self.FORMAT)


serializer = SerializationMiddleware()
serializer.register_serializer(DateTimeSerializer(), 'TinyDate')


def listsearch(query, item):
    """Return match with query on an item from the list of input/output files

    The lists of input and output files can consist either of file names
    (strings), or lists containing the filename and the hash of the file (if
    hashing is enabled). This function provides a transparent interface to
    these two options.

    Parameters:
        query : str
            The search query
        item : str or list containing two strings
            A file name or a list containing a file name and hash

    Returns:
        boolean
    """
    fh = ''
    if not isinstance(item, six.string_types):
        fh = item[1]
        item = item[0]

    return bool(re.search(query, item) or
                re.search(query, fh))
