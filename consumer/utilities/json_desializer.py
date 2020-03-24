import json

class JsonDeserializer:
    """Json de-serializer provide functions for kafka value deserialization in
    json format
    """
    @staticmethod
    def deserializer_func(x):
        """
        Args:
            x:
        """
        return json.loads(x.decode('utf-8'))