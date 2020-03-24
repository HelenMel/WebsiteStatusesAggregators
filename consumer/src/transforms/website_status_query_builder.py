from typing import Tuple, Any
from consumer.dto.website_status import WebsiteStatus
import uuid

class WebsiteStatusToSQLBuilder():
    def build(self, item: WebsiteStatus) -> (str, Tuple[Any, ...]):
        """ Build SQL request from item
        :param item: status that needs to be transformed to a query
        :return: Tuple(query, record) that together made a full request
        """
        record = (item.id, item.url, (item.occured_at / 1000.0), item.response_time, item.error_code)
        query = """
            INSERT INTO website_status(id, url, occured_at, response_time, error_code)
            VALUES(%s, %s, to_timestamp(%s), %s, %s)
            """
        return (query, record)

