from kafka import KafkaConsumer
import logging
from typing import Optional, Callable
from consumer.dto.website_status import WebsiteStatus

logger = logging.getLogger(__name__)

class KafkaTopicReader():

    def __init__(self,
                 topic_name: str,
                 group_id: str,
                 deserializer_func: Callable,
                 auto_offset_reset='earliest',
                 enable_auto_commit=True,
                 ):
        self.topic_name = topic_name
        self.group_name = group_id
        self.deserializer_func = deserializer_func
        self.auto_offset_reset = auto_offset_reset
        self.enable_auto_commit = enable_auto_commit
        self._consumer = None

    @property
    def consumer(self):
        if self._consumer is None:
            self._consumer = KafkaConsumer(self.topic_name,
                                       bootstrap_servers=['localhost:9092'],
                                       auto_offset_reset=self.auto_offset_reset,
                                       enable_auto_commit=self.enable_auto_commit,
                                       group_id=self.group_name,
                                       value_deserializer=self.deserializer_func)
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
            logger.error("Read batch unknown exception", err)
            return None

    def close(self) -> None:
        self.consumer.close()





