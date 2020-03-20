from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError
import logging

logger = logging.getLogger(__name__)

class KafkaTopicPublisher():

    def __init__(self):
        self._producer = None

    '''Blocking sync function that send exactly one message
    '''
    def send_sync(self, topic_name, event) -> None:
        if self._producer is None:
            logger.error("Producer are not started yet. Run 'connect'")
            return
        try:
            future = self._producer.send(topic_name, event)
            result = future.get(timeout=20)
            logger.debug(f"Message saved to partition: {result.partition} with offset: {result.offset}")
        except KafkaTimeoutError as timeout_err:
            logger.error("Kafka send timeout", timeout_err)
        except Exception as err:
            logger.error("Kafka send unknown error", err)

    def connect(self, serializer_func) -> None:
        self._producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                       value_serializer=serializer_func)