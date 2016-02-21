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
