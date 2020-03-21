import psycopg2
import logging
import uuid

logger = logging.getLogger(__name__)

class PostgresqlWriter():

    def __init__(self):
        self._conn = None
        self._cursor = None

    @property
    def conn(self):
        if self._conn is None or self._conn.closed:
            try:
                self._conn = psycopg2.connect(user = 'developer',
                                              password= '12345',
                                              host = '0.0.0.0',
                                              port = '5433',
                                              database = 'website_statuses')
            except (Exception, psycopg2.Error) as err:
                logger.exception(f'Error connecting to PostgreSQL {str(err)}')
                raise err
        return self._conn

    def send_sync(self, item) -> None:
        try:
            self._cursor = self.conn.cursor()
            query = """INSERT INTO website_status(id, url, occured_at, response_time, error_code)
                              VALUES(%s, %s, to_timestamp(%s), %s, %s)"""
            record = (str(uuid.uuid4()), item.url, (item.occured_at / 1000.0), item.response_time, item.error_code)
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










