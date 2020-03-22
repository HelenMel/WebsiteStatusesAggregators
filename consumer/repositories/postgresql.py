import psycopg2
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
            except (Exception, psycopg2.Error) as err:
                logger.exception(f'Error connecting to PostgreSQL {str(err)}')
                raise err
        return self._conn

    def send_sync(self, item) -> None:
        try:
            self._cursor = self.conn.cursor()
            query, record = self.item_query_builder.build(item)
            self._cursor.execute(query, record)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as err:
            logger.exception(f'Database error {str(err)}')
            raise err
        finally:
            self.close()

    ''' Close database connections
    '''
    def close(self) -> None:
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._conn:
            self._conn.close()
            self._conn = None










