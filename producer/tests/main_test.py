import time
from unittest import TestCase
from unittest.mock import Mock, patch
import requests
import unittest
import schedule
from producer.__main__ import WebsiteStatusProducer
from tests.mocked_response import MockedResponse

class TestProducerIntegration(TestCase):
    @patch('producer.checkers.website_checker.requests')
    def test_one_website_success(self, mock_request):
        mock_request.get.return_value = MockedResponse(5, 200)
        # it is hard to use real kafka in tests, so lets mock it
        publisher = Mock()
        sut = WebsiteStatusProducer(['http://google.com'], 1)
        sut._publisher = publisher

        # test that called at least twice.
        def stop():
            sut.is_running = False
        schedule.every(3).seconds.do(stop)
        sut.run()

        self.assertEqual(publisher.send_sync.call_count, 2)

    @patch('producer.checkers.website_checker.requests')
    def test_many_websites_success(self, mock_request):
        mock_request.get.return_value = MockedResponse(5, 200)
        # it is hard to use real kafka in tests, so lets mock it
        publisher = Mock()
        sut = WebsiteStatusProducer(['http://google.com',
                                     'https://stackoverflow.com',
                                     'https://docs.python.org/'], 1)
        sut._publisher = publisher

        # test that called at least twice.
        def stop():
            sut.is_running = False

        schedule.every(3).seconds.do(stop)
        sut.run()

        # 3 websites should publish events 2 times each
        self.assertEqual(publisher.send_sync.call_count, 6)

    @patch('producer.checkers.website_checker.requests')
    def test_one_website_error(self, mock_request):
        mock_request.get.side_effect = Exception
        # it is hard to use real kafka in tests, so lets mock it
        publisher = Mock()
        sut = WebsiteStatusProducer(['http://google.com'], 1)
        sut._publisher = publisher

        # test that called at least twice.
        def stop():
            sut.is_running = False

        schedule.every(3).seconds.do(stop)
        sut.run()

        self.assertEqual(publisher.send_sync.call_count, 0)

