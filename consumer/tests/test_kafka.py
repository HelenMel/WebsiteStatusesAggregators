from unittest import TestCase
from consumer.repositories.kafka import KafkaTopicReader, ReadOneError
from consumer.config.app_config import KafkaConfig
from unittest.mock import MagicMock
from collections import namedtuple

topic = 'greetings'
group_id = 'everyone'
config = KafkaConfig('localhost:9092', topic, 'earliest', True, group_id, None, None, None, None)
class TestKafkaTopicReader(TestCase):
    def test_read_one_success(self):
        sut = KafkaTopicReader(config, str)
        sent_event = Message({'url': 'http://google.com',
                      'occured_at': 1585037107,
                      'response_time': 11,
                      'error_code': 404})
        sut._consumer = MagicMock()
        sut._consumer.__next__.return_value = sent_event
        response = sut.read_one()

        self.assertEqual(response.url,  'http://google.com')
        self.assertEqual(response.occured_at, 1585037107)
        self.assertEqual(response.response_time, 11)
        self.assertEqual(response.error_code, 404)

    def test_read_one_no_new_messages(self):
        sut = KafkaTopicReader(config, str)
        sut._consumer = MagicMock()
        sut._consumer.__next__.side_effect = StopIteration
        response = sut.read_one()

        self.assertIsNone(response)

    def test_read_one_error(self):
        sut = KafkaTopicReader(config, str)
        sut._consumer = MagicMock()
        sut._consumer.__next__.side_effect = ReadOneError('unknown problem')

        with self.assertRaises(ReadOneError):
            response = sut.read_one()
            self.assertIsNone(response)

Message = namedtuple('Message', 'value')
