from dataclasses import dataclass
from typing import Optional
import os
from pathlib import Path

@dataclass
class KafkaConfig:
    bootstrap_server: str
    request_timeout: int
    conn_close_timeout: int
    main_topic_name: str
    security_protocol: Optional[str]
    ssl_cafile: Optional[str]
    ssl_certfile: Optional[str]
    ssl_keyfile: Optional[str]

class AppConfig():

    def kafka_config(self) -> KafkaConfig:
        home = str(Path.home())
        ssl_cafile = os.path.join(home, 'kafka/cert/ca.pem')
        ssl_certfile = os.path.join(home, 'kafka/cert/service.cert')
        ssl_keyfile = os.path.join(home, 'kafka/cert/service.key')
        return KafkaConfig(
            bootstrap_server='kafka-3cf2d9b6-to-62fc.aivencloud.com:23705',
            request_timeout=10,
            conn_close_timeout=3,
            main_topic_name='WebsiteStatus',
            security_protocol='SSL',
            ssl_cafile=ssl_cafile,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile
        )





