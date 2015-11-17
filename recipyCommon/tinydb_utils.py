import datetime

from tinydb.storages import JSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware


class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime.datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')



serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
