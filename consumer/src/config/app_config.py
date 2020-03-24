from configparser import ConfigParser
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
        main_topic_name = self.conf_parser.get('kafka', 'main_topic_name')
        auto_offset_reset = self.conf_parser.get('kafka', 'auto_offset_reset')
        enable_auto_commit = self.conf_parser.getboolean('kafka', 'enable_auto_commit')
        group_id = self.conf_parser.get('kafka', 'group_id')

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
                           main_topic_name,
                           auto_offset_reset,
                           enable_auto_commit,
                           group_id,
                           security_protocol,
                           ssl_cafile,
                           ssl_certfile,
                           ssl_keyfile)

    def postgresql_config(self) -> PostgresqlConfig:
        home = str(Path.home())
        user = self.conf_parser.get('postgresql', 'user')
        host = self.conf_parser.get('postgresql', 'host')
        port = self.conf_parser.get('postgresql', 'port')
        database = self.conf_parser.get('postgresql', 'database')
        if self.conf_parser.has_option('postgresql', 'password_path'):
            password_file = os.path.join(home,self.conf_parser.get('postgresql', 'password_path'))
            f = open(password_file, 'r')
            password = f.read()
        elif self.conf_parser.has_option('postgresql', 'password'):
            password = self.conf_parser.get('postgresql', 'password')
        else:
            password = None
        ssl = None
        if self.conf_parser.has_option('postgresql', 'ssl'):
            ssl = self.conf_parser.get('postgresql', 'ssl')
        return PostgresqlConfig(user,
                                host,
                                port,
                                database,
                                ssl,
                                password)






