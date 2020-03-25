from dataclasses import dataclass
from typing import Optional
import os
from pathlib import Path

@dataclass
class KafkaConfig:
    bootstrap_server: str
    main_topic_name: str
    auto_offset_reset: str
    enable_auto_commit: bool
    group_id: str
    security_protocol: Optional[str]
    ssl_cafile: Optional[str]
    ssl_certfile: Optional[str]
    ssl_keyfile: Optional[str]

@dataclass
class PostgresqlConfig:
    user: str
    host: str
    port: str
    database: str
    ssl: Optional[str]
    password: Optional[str]

class AppConfig():

    def kafka_config(self) -> KafkaConfig:
        home = str(Path.home())
        ssl_cafile = os.path.join(home, 'kafka/cert/ca.pem')
        ssl_certfile = os.path.join(home, 'kafka/cert/service.cert')
        ssl_keyfile = os.path.join(home, 'kafka/cert/service.key')
        return KafkaConfig(
            bootstrap_server='kafka-3cf2d9b6-to-62fc.aivencloud.com:23705',
            main_topic_name='WebsiteStatus',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='postgres_dev',
            security_protocol='SSL',
            ssl_cafile=ssl_cafile,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile
        )

    def postgresql_config(self) -> PostgresqlConfig:
        home = str(Path.home())
        password_file = os.path.join(home, 'kafka/pass/avnadm.pgpass')
        f = open(password_file, 'r')
        password = f.read()
        return PostgresqlConfig(
            user='avnadmin',
            host='pg-19c06e19-to-62fc.aivencloud.com',
            port='23703',
            database='website_statuses',
            ssl='require',
            password=password
        )





