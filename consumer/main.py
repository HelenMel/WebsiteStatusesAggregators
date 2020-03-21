from consumer.repositories.kafka import KafkaTopicReader
from consumer.repositories.postgresql import PostgresqlWriter
import json
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    print("start consumer")
    topic = "WebsiteStatus"
    group = 'my_group'
    db_writer = PostgresqlWriter()
    def deserializer_func(x):
        return json.loads(x.decode('utf-8'))

    reader = KafkaTopicReader(topic, group, deserializer_func)
    while True:
        try:
            status = reader.read_one()
            if status is not None:
                print(status)
                db_writer.send_sync(status)
                print('Anything else')
        except KeyboardInterrupt as _:
            break
        except Exception as err:
            logger.error("Unknown exception", err)
            break
    reader.close()