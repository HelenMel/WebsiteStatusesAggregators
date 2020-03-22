from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError
from typing import Callable
from config.app_config import KafkaConfig
import logging

logger = logging.getLogger(__name__)

class KafkaWriter():

    def __init__(self, config: KafkaConfig, serializer_func: Callable):
        self._producer = None
        self.config = config
        self.serializer_func = serializer_func

    @property
    def producer(self):
        if self._producer is None:
            self._producer = KafkaProducer(bootstrap_servers=[self.config.bootstrap_server],
                                           value_serializer=self.serializer_func)
        return self._producer

    '''Blocking sync function that send exactly one message
    '''
    def send_sync(self, event, topic_name=None) -> None:
        if topic_name is None:
            topic_name = self.config.main_topic_name

        try:
            future = self.producer.send(topic_name, event)
            result = future.get(timeout=self.config.request_timeout)
            logger.debug(f"Message saved to partition: {result.partition} with offset: {result.offset}")
        except KafkaTimeoutError as timeout_err:
            logger.error(f"Kafka send timeout {str(timeout_err)}")
        except Exception as err:
            logger.error(f"Kafka send unknown error {str(err)}")

    def close(self) -> None:
        if self._producer:
            self._producer.close(timeout=self.config.conn_close_timeout)
            self._producer = None
