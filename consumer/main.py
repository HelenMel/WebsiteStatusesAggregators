from consumer.repositories.kafka import KafkaTopicReader
from consumer.repositories.postgresql import PostgresqlWriter
from consumer.transforms.website_status_query_builder import WebsiteStatusToSQLBuilder
from consumer.config.app_config import AppConfig
from consumer.utilities.json_desializer import JsonDeserializer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebsiteStatusConsumer():
    """ this class read events from kafka and stores to a postgresql db"""
    def __init__(self):
        self.is_running = False
        self._consumer = None
        self._app_config = None
        self._db_writer = None

    @property
    def app_config(self):
        if self._app_config is None:
            self._app_config = AppConfig()
        return self._app_config

    @property
    def consumer(self):
        if self._consumer is None:
            self._consumer = KafkaTopicReader(self.app_config.kafka_config(), JsonDeserializer.deserializer_func)
        return self._consumer

    @property
    def db_writer(self):
        if self._db_writer is None:
            query_builder = WebsiteStatusToSQLBuilder()
            self._db_writer = PostgresqlWriter(self.app_config.postgresql_config(), query_builder)
        return self._db_writer

    def run(self):
        logger.info("start consumer")
        self.is_running = True

        while self.is_running:
            try:
                status = self.consumer.read_one()
                if status is not None:
                    print(status)
                    self.db_writer.send_sync(status)
                    logger.info(f"Status saved to postgres {status}")
            except KeyboardInterrupt as _:
                break
            except Exception as err:
                logger.error(f"Unknown exception str{err}")
                break
        self.consumer.close()
        self.db_writer.close()


if __name__ == '__main__':
    consumer = WebsiteStatusConsumer()
    consumer.run()
