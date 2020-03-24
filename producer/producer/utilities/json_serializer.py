import dataclasses
import json

class JsonSerializer:
    """Json serializer provide functions for kafka value serialization in json
    format
    """
    @staticmethod
    def dataclass_to_json(event) -> str:
        """
        Args:
            event:
        """
        return json.dumps(dataclasses.asdict(event)).encode('utf-8')