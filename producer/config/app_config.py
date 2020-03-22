from configparser import ConfigParser
from dataclasses import dataclass
import os

@dataclass
class KafkaConfig:
    bootstrap_server: str
    request_timeout: int
    conn_close_timeout: int
    main_topic_name: str

@dataclass
class SchedulerConfig:
    request_status_every_sec: int

class AppConfig():

    def __init__(self):
        self._conf_parser = None
        self._ini_file = None

    @property
    def ini_file(self):
        if self._ini_file is None:
            this_folder = os.path.dirname(os.path.abspath(__file__))
            self._ini_file = os.path.join(this_folder, 'config-dev.ini')
        return self._ini_file

    @property
    def conf_parser(self):
        if self._conf_parser is None:
            self._conf_parser = ConfigParser()
            self._conf_parser.read(self.ini_file)
        return self._conf_parser

    def kafka_config(self) -> KafkaConfig:
        bootstrap_server = self.conf_parser.get('kafka', 'bootstrap_server')
        request_timeout = self.conf_parser.getint('kafka', 'request_timeout')
        conn_close_timeout = self.conf_parser.getint('kafka', 'conn_close_timeout')
        main_topic_name = self.conf_parser.get('kafka', 'main_topic_name')
        return KafkaConfig(bootstrap_server, request_timeout, conn_close_timeout, main_topic_name)


    def scheduler_config(self) -> SchedulerConfig:
        request_status_every_sec = self.conf_parser.getint('scheduler', 'request_status_every_sec')
        return SchedulerConfig(request_status_every_sec)






