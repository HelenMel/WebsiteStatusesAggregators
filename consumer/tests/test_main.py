from unittest import TestCase
from unittest.mock import Mock
from consumer.main import WebsiteStatusConsumer
import schedule
from threading import Thread
from time import sleep


class TestWebsiteStatusConsumer(TestCase):
    def test_run_success(self):
        # it is hard to use real kafka in tests, so lets mock it
        consumer = Mock()
        consumer.read_one.return_value = 'Message from Kafka'
        db_writer = Mock()
        sut = WebsiteStatusConsumer()
        sut._consumer = consumer
        sut._db_writer = db_writer

        thread = Thread(target=sut.run)
        thread.start()
        sleep(0.001)
        sut.is_running = False
        thread.join()

        db_writer.send_sync.assert_called_with('Message from Kafka')

    def test_run_no_messages(self):
        # it is hard to use real kafka in tests, so lets mock it
        consumer = Mock()
        consumer.read_one.return_value = None
        db_writer = Mock()
        sut = WebsiteStatusConsumer()
        sut._consumer = consumer
        sut._db_writer = db_writer

        thread = Thread(target=sut.run)
        thread.start()
        sleep(0.001)
        sut.is_running = False
        thread.join()

        db_writer.send_sync.assert_not_called()

    def test_run_no_error(self):
        # it is hard to use real kafka in tests, so lets mock it
        consumer = Mock()
        consumer.read_one.side_effect = Exception
        db_writer = Mock()
        sut = WebsiteStatusConsumer()
        sut._consumer = consumer
        sut._db_writer = db_writer

        thread = Thread(target=sut.run)
        thread.start()
        sleep(0.001)
        sut.is_running = False
        thread.join()

        db_writer.send_sync.assert_not_called()