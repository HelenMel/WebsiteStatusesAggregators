from unittest import TestCase
from producer.repositories.kafka import KafkaWriter
from producer.config.app_config import KafkaConfig
from kafka.errors import KafkaTimeoutError
from unittest.mock import Mock, MagicMock
from collections import namedtuple

timeout = 101
topic = 'greetings'
msg = 'Hello'
config = KafkaConfig('localhost:9092', timeout, 22, topic, None, None, None, None)

class TestKafkaWriterSendSync(TestCase):

    def test_send_sync_success(self):
        sut = KafkaWriter(config, str)
        future_mock = Mock()
        future_mock.get.return_value = KafkaTestResponse('0034', '2')
        sut._producer = MagicMock()
        sut._producer.send.return_value=future_mock

        sut.send_sync(msg)

        sut._producer.send.assert_called_once_with(topic, msg)
        future_mock.get.assert_called_once_with(timeout=timeout)

    def test_send_sync_timeout_error(self):
        sut = KafkaWriter(config, str)
        future_mock = Mock()
        future_mock.get.side_effect = KafkaTimeoutError()
        sut._producer = MagicMock()
        sut._producer.send.return_value = future_mock

        with self.assertRaises(KafkaTimeoutError):
            sut.send_sync(msg)
            sut._producer.send.assert_called_once_with(topic, msg)
            future_mock.get.assert_called_once_with(timeout=timeout)

    def test_send_sync_timeout_unknown_error(self):
        sut = KafkaWriter(config, str)
        future_mock = Mock()
        future_mock.get.side_effect = Exception()
        sut._producer = MagicMock()
        sut._producer.send.return_value = future_mock

        with self.assertRaises(Exception):
            sut.send_sync(msg)
            sut._producer.send.assert_called_once_with(topic, msg)
            future_mock.get.assert_called_once_with(timeout=timeout)

KafkaTestResponse = namedtuple('KafkaResponse', ['offset', 'partition'])
