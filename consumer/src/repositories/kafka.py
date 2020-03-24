from kafka import KafkaConsumer
import logging
from typing import Optional, Callable
from consumer.dto.website_status import WebsiteStatus
from consumer.config.app_config import KafkaConfig

logger = logging.getLogger(__name__)

class ConsumerCreationError(Exception):
    def __init__(self, message):
        self.message = message

class ReadOneError(Exception):
    def __init__(self, message):
        self.message = message

class KafkaTopicReader():

    def __init__(self, config: KafkaConfig, deserializer_func: Callable):
        self.config = config
        self.deserializer_func = deserializer_func
        self._consumer = None

    @property
    def consumer(self):
        if self._consumer is None:
            security_protocol = self.config.security_protocol
            if security_protocol is None:
                self._consumer = KafkaConsumer(self.config.main_topic_name,
                                               bootstrap_servers=[self.config.bootstrap_server],
                                               auto_offset_reset=self.config.auto_offset_reset,
                                               enable_auto_commit=self.config.enable_auto_commit,
                                               group_id=self.config.group_id,
                                               value_deserializer=self.deserializer_func)
            elif security_protocol == 'SSL':
                self._consumer = KafkaConsumer(self.config.main_topic_name,
                                               bootstrap_servers=[self.config.bootstrap_server],
                                               auto_offset_reset=self.config.auto_offset_reset,
                                               enable_auto_commit=self.config.enable_auto_commit,
                                               group_id=self.config.group_id,
                                               ssl_check_hostname=True,
                                               security_protocol=security_protocol,
                                               ssl_cafile=self.config.ssl_cafile,
                                               ssl_certfile=self.config.ssl_certfile,
                                               ssl_keyfile=self.config.ssl_keyfile,
                                               value_deserializer=self.deserializer_func)
            else:
                raise ConsumerCreationError("Unknown security protocol")
        return self._consumer


    def read_one(self) -> Optional[WebsiteStatus]:
        try:
            message = next(self.consumer)
            status = WebsiteStatus.from_dict(message.value)
            return status
        except StopIteration:
            # if StopIteration is raised, then no new messages available. Not an error
            return None
        except Exception as err:
            raise ReadOneError(f"Read batch unknown exception {str(err)}")

    def close(self) -> None:
        self.consumer.close()





