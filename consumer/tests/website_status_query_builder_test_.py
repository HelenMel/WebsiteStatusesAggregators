from unittest import TestCase
from consumer.dto.website_status import WebsiteStatus
from consumer.transforms.website_status_query_builder import WebsiteStatusToSQLBuilder

class TestWebsiteStatusToSQLBuilder(TestCase):
    def test_build(self):
        expected_query = """
            INSERT INTO website_status(id, url, occured_at, response_time, error_code)
            VALUES(%s, %s, to_timestamp(%s), %s, %s)
            """
        item = WebsiteStatus('id1', 'http://google.com', 1200, 23, 404)

        builder = WebsiteStatusToSQLBuilder()

        query, record = builder.build(item)
        self.assertEqual(query, expected_query)
        self.assertEqual(record, ('id1', 'http://google.com', 1.2, 23, 404))
