import time
from unittest import TestCase
import requests
import unittest
import schedule
from producer.main import WebsiteStatusProducer

class TestProducerIntegration(TestCase):
    def test_one_website_success(self):
        sut = WebsiteStatusProducer(['http://google.com'], 1)
        # mock kafka
        # test that called at least twice.

        def stop():
            sut.is_running = False
        schedule.every(10).seconds.do(stop)
        sut.run()
        tearDownModule(compose)

