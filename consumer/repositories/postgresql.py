import psycopg2
from  psycopg2 import OperationalError, DatabaseError
import logging
from consumer.config.app_config import PostgresqlConfig

logger = logging.getLogger(__name__)

class PostgresqlWriter():

    def __init__(self, config: PostgresqlConfig , item_query_builder):
        self._conn = None
        self._cursor = None
        self.config = config
        self.item_query_builder = item_query_builder

    @property
    def conn(self):
        if self._conn is None or self._conn.closed:
            try:
                self._conn = psycopg2.connect(user = self.config.user,
                                              sslmode = self.config.ssl,
                                              password= self.config.password,
                                              host = self.config.host,
                                              port = self.config.port,
                                              database = self.config.database)
            except OperationalError as err:
                logger.error(f'PostgreSQL operational error {str(err)}')
                raise err
            except Exception as err:
                logger.error(f'Unknown error during connection to PostgreSQL {str(err)}')
                raise err
        return self._conn

    def send_sync(self, item) -> None:
        """ Send input transaction to postgresql.

        :param item: any items that item_query_builder could accept
        :return: None
        """
        try:
            self._cursor = self.conn.cursor()
            query, record = self.item_query_builder.build(item)
            self._cursor.execute(query, record)
            self.conn.commit()
        except (Exception, DatabaseError) as err:
            logger.error(f'Database error {str(err)}')
            self.close()
            raise err

    def close(self) -> None:
        """ Close database connections"""
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._conn:
            self._conn.close()
            self._conn = None










