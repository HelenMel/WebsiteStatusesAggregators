from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError
from typing import Callable
from producer.config.app_config import KafkaConfig
import logging

logger = logging.getLogger(__name__)

class ProducerCreationError(Exception):
    def __init__(self, message):
        self.message = message

class KafkaWriter():

    def __init__(self, config: KafkaConfig, serializer_func: Callable):
        self._producer = None
        self.config = config
        self.serializer_func = serializer_func

    @property
    def producer(self):
        if self._producer is None:
            security_protocol = self.config.security_protocol
            if security_protocol is None:
                self._producer = KafkaProducer(bootstrap_servers=[self.config.bootstrap_server],
                                               value_serializer=self.serializer_func)
            elif security_protocol == 'SSL':
                self._producer = KafkaProducer(bootstrap_servers=[self.config.bootstrap_server],
                                                ssl_check_hostname=True,
                                                security_protocol = security_protocol,
                                                ssl_cafile= self.config.ssl_cafile,
                                                ssl_certfile = self.config.ssl_certfile,
                                                ssl_keyfile = self.config.ssl_keyfile,
                                                value_serializer=self.serializer_func)
            else:
                logger.error("Unknown security protocol")
                raise ProducerCreationError("Unknown security protocol")
        return self._producer

    def send_sync(self, event, topic_name=None) -> None:
        """Blocking sync function that send exactly one message to kafka

        :param event: any events that could be serialized with serializer_func
        :param topic_name: name of the topic to store event
        :return:
        """
        if topic_name is None:
            topic_name = self.config.main_topic_name

        try:
            future = self.producer.send(topic_name, event)
            result = future.get(timeout=self.config.request_timeout)
            logger.debug(f"Message saved to partition: {result.partition} with offset: {result.offset}")
        except KafkaTimeoutError as timeout_err:
            logger.error(f"Kafka send timeout {str(timeout_err)}")
            raise KafkaTimeoutError
        except Exception as err:
            logger.error(f"Kafka send unknown error {str(err)}")
            raise err

    def close(self) -> None:
        if self._producer:
            self._producer.close(timeout=self.config.conn_close_timeout)
            self._producer = None

