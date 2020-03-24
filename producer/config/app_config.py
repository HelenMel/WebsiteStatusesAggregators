from configparser import ConfigParser
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

    def __init__(self):
        self._conf_parser = None
        self._ini_file = None
        self._env = None

    @property
    def env(self):
        if self._env is None:
            self._env = os.getenv('ENV', 'dev')
        return self._env

    @property
    def ini_file(self):
        if self._ini_file is None:
            if self.env == 'live':
                file_name = 'config-live.ini'
            else:
                file_name = 'config-dev.ini'
            this_folder = os.path.dirname(os.path.abspath(__file__))
            self._ini_file = os.path.join(this_folder, file_name)
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

        home = str(Path.home())
        security_protocol = ssl_cafile = ssl_certfile = ssl_keyfile = None
        if self.conf_parser.has_option('kafka', 'security_protocol'):
            security_protocol = self.conf_parser.get('kafka', 'security_protocol')
        if self.conf_parser.has_option('kafka', 'ssl_cafile'):
            ssl_cafile = os.path.join(home, self.conf_parser.get('kafka', 'ssl_cafile'))
        if self.conf_parser.has_option('kafka', 'ssl_certfile'):
            ssl_certfile = os.path.join(home, self.conf_parser.get('kafka', 'ssl_certfile'))
        if self.conf_parser.has_option('kafka', 'ssl_keyfile'):
            ssl_keyfile = os.path.join(home,self.conf_parser.get('kafka', 'ssl_keyfile'))
        return KafkaConfig(bootstrap_server,
                           request_timeout,
                           conn_close_timeout,
                           main_topic_name,
                           security_protocol,
                           ssl_cafile,
                           ssl_certfile,
                           ssl_keyfile)






