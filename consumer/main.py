from consumer.repositories.kafka import KafkaTopicReader
from consumer.repositories.postgresql import PostgresqlWriter
from consumer.transforms.website_status_query_builder import WebsiteStatusToSQLBuilder
from consumer.config.app_config import AppConfig
from consumer.utilities.json_desializer import JsonDeserializer
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("start consumer")
    app_config = AppConfig()
    query_builder = WebsiteStatusToSQLBuilder()
    db_writer = PostgresqlWriter(app_config.postgresql_config(), query_builder)

    reader = KafkaTopicReader(app_config.kafka_config(), JsonDeserializer.deserializer_func)
    while True:
        try:
            status = reader.read_one()
            if status is not None:
                print(status)
                db_writer.send_sync(status)
                print('send')
        except KeyboardInterrupt as _:
            break
        except Exception as err:
            logger.error(f"Unknown exception str{err}")
            break
    reader.close()