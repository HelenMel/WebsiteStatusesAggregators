from unittest import TestCase
from producer.checkers.website_checker import WebsiteChecker
from producer.tests.mocked_response import MockedResponse
from unittest.mock import patch
from requests.exceptions import Timeout

class TestWebsiteChecker(TestCase):

    @patch('producer.checkers.website_checker.requests')
    def test_check_get_success(self, mock_request):
        mock_request.get.return_value = MockedResponse(5, 200)
        sut = WebsiteChecker('http://google.com')
        answer = sut.check_get()

        self.assertIsNotNone(answer)
        self.assertEqual(answer.url, 'http://google.com')
        self.assertEqual(answer.response_time, 5 * 1000)
        self.assertIsNone(answer.error_code)

    @patch('producer.checkers.website_checker.requests')
    def test_check_get_http_error(self, mock_request):
        mock_request.get.return_value = MockedResponse(3, 503, error=True)
        sut = WebsiteChecker('http://google.com')
        answer = sut.check_get()

        self.assertIsNotNone(answer)
        self.assertEqual(answer.url, 'http://google.com')
        self.assertEqual(answer.response_time, 3 * 1000)
        self.assertEqual(answer.error_code, 503)

    @patch('producer.checkers.website_checker.requests')
    def test_check_get_unknown_error(self, mock_request):
        mock_request.get.side_effect = Timeout
        sut = WebsiteChecker('http://google.com')

        answer = sut.check_get()
        self.assertIsNone(answer)