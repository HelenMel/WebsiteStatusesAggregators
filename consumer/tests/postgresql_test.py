from unittest import TestCase
from unittest.mock import patch, Mock, ANY, MagicMock
from consumer.repositories.postgresql import PostgresqlWriter
from consumer.config.app_config import PostgresqlConfig
import psycopg2

config = PostgresqlConfig('developer', '0.0.0.0', '5433', 'website_statuses', None, None)
class TestPostgresqlWriterConnect(TestCase):

    @patch('consumer.repositories.postgresql.psycopg2')
    def test_conn(self, mock_psycopg2):
        conn_mock = Mock()
        mock_psycopg2.connect.return_value = conn_mock

        sut = PostgresqlWriter(config, ANY)
        result = sut.conn

        self.assertEqual(result, conn_mock)

    @patch('consumer.repositories.postgresql.psycopg2')
    def test_conn_error(self, mock_psycopg2):
        mock_psycopg2.connect.side_effect = psycopg2.OperationalError()

        sut = PostgresqlWriter(config, ANY)
        with self.assertRaises(psycopg2.OperationalError):
            _ = sut.conn


class TestPostgresqlWriterSendSync(TestCase):
    item = 'http://google.com'
    query = 'INSERT INTO website_status(id, url) VALUES(%s, %s)'
    record = (1, 'http://google.com')

    @patch('consumer.repositories.postgresql.psycopg2')
    def test_send_sync_success(self, mock_psycopg2):
        query_builder = Mock()
        query_builder.build.return_value = (self.query, self.record)
        cursor = Mock()
        conn_mock = MagicMock()
        conn_mock.closed.return_value = False
        conn_mock.cursor.return_value = cursor
        mock_psycopg2.connect.return_value = conn_mock

        sut = PostgresqlWriter(config, query_builder)

        sut.send_sync(self.item)

        query_builder.build.assert_called_once_with(self.item)
        conn_mock.commit.assert_called_once()
        cursor.execute.assert_called_once_with(self.query, self.record)

    @patch('consumer.repositories.postgresql.psycopg2')
    def test_send_sync_failure_cursor(self, mock_psycopg2):
        conn_mock = MagicMock()
        conn_mock.closed.return_value = False
        conn_mock.cursor.side_effect = psycopg2.DatabaseError()
        mock_psycopg2.connect.return_value = conn_mock

        sut = PostgresqlWriter(config, ANY)

        with self.assertRaises(psycopg2.DatabaseError):
            _ = sut.send_sync(self.item)
        conn_mock.close.assert_called_once()

    @patch('consumer.repositories.postgresql.psycopg2')
    def test_send_sync_failure_execute(self, mock_psycopg2):
        query_builder = Mock()
        query_builder.build.return_value = (self.query, self.record)
        cursor = Mock()
        cursor.execute.side_effect = psycopg2.DatabaseError()
        conn_mock = MagicMock()
        conn_mock.closed.return_value = False
        conn_mock.cursor.return_value = cursor
        mock_psycopg2.connect.return_value = conn_mock

        sut = PostgresqlWriter(config, query_builder)

        with self.assertRaises(psycopg2.DatabaseError):
            sut.send_sync(self.item)

        query_builder.build.assert_called_once_with(self.item)
        conn_mock.commit.assert_not_called()
        conn_mock.close.assert_called_once()
        cursor.execute.assert_called_once_with(self.query, self.record)


class TestPostgresqlWriterClose(TestCase):
    def test_close(self):
        conn_mock = MagicMock()
        sut = PostgresqlWriter(config, ANY)

        sut._cursor = conn_mock
        sut.close()
        conn_mock.close.assert_called_once()

