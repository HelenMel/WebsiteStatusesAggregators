from typing import Tuple, Any
from dto.website_status import WebsiteStatus
import uuid

class WebsiteStatusToSQLBuilder():
    def build(self, item: WebsiteStatus) -> (str, Tuple[Any, ...]):
        """
        Args:
            item (WebsiteStatus):
        """
        record = (str(uuid.uuid4()), item.url, (item.occured_at / 1000.0), item.response_time, item.error_code)
        query = """
            INSERT INTO website_status(id, url, occured_at, response_time, error_code)
            VALUES(%s, %s, to_timestamp(%s), %s, %s)
            """
        return (query, record)

