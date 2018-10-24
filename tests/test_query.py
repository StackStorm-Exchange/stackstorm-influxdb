from influxdb_base_action_test_case import InfluxDBBaseActionTestCase
from lib.base_action import BaseAction
from lib.query import QueryAction

import mock


class TestActionLibQueryAction(InfluxDBBaseActionTestCase):
    __test__ = True
    action_cls = QueryAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, QueryAction)
        self.assertIsInstance(action, BaseAction)

    def test_detect_query_method_select(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('SELECT * FROM mydatabase')
        self.assertEquals(result, 'GET')

    def test_detect_query_method_select_into(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('SELECT * FROM mydatabase INTO another')
        self.assertEquals(result, 'POST')

    def test_detect_query_method_show(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('SHOW databases')
        self.assertEquals(result, 'GET')

    def test_detect_query_method_alter(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('ALTER database ADD COLUMN new')
        self.assertEquals(result, 'POST')

    def test_detect_query_method_create(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('CREATE DATABASE newdata')
        self.assertEquals(result, 'POST')

    def test_detect_query_method_delete(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('DELETE DATABASE newdata')
        self.assertEquals(result, 'POST')

    def test_detect_query_method_drop(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('DROP DATABASE newdata')
        self.assertEquals(result, 'POST')

    def test_detect_query_method_grant(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('GRANT ALL TO user')
        self.assertEquals(result, 'POST')

    def test_detect_query_method_kill(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('KILL data IN database')
        self.assertEquals(result, 'POST')

    def test_detect_query_method_revoke(self):
        action = self.get_action_instance({})
        result = action.detect_query_method('REVOKE ALL FROM user')
        self.assertEquals(result, 'POST')

    def test_detect_query_method_junk(self):
        action = self.get_action_instance({})
        with self.assertRaises(ValueError):
            action.detect_query_method('SOMETHING other nonvalid query')

    def test_extract_results(self):
        action = self.get_action_instance({})
        data = [mock.MagicMock(raw='a'),
                mock.MagicMock(raw='b'),
                mock.MagicMock(raw='c')]
        result = action.extract_results(data)
        self.assertEquals(result, ['a', 'b', 'c'])

    def test_extract_results_not_list(self):
        action = self.get_action_instance({})
        data = mock.MagicMock(raw='a')
        result = action.extract_results(data)
        self.assertEquals(result, ['a'])

    @mock.patch('lib.query.QueryAction.make_client')
    def test_run(self, mock_make_client):
        action = self.get_action_instance({})

        # mock
        mock_client = mock.MagicMock()
        mock_client.query.return_value = mock.MagicMock(raw='expected')
        mock_make_client.return_value = mock_client

        # run
        result = action.run(query="SELECT * FROM database",
                            chunked=None,
                            database='database',
                            epoch=None,
                            method=None)

        # assert
        self.assertEquals(result, ['expected'])
        mock_client.query.assert_called_with("SELECT * FROM database",
                                             database='database',
                                             epoch=None,
                                             chunked=False,
                                             chunk_size=0,
                                             method="GET")

    @mock.patch('lib.query.QueryAction.make_client')
    def test_run_method_override(self, mock_make_client):
        action = self.get_action_instance({})

        # mock
        mock_client = mock.MagicMock()
        mock_client.query.return_value = mock.MagicMock(raw='expected')
        mock_make_client.return_value = mock_client

        # run
        result = action.run(query="DROP DATABASE data",
                            chunked=None,
                            database='data',
                            epoch=None,
                            method='POST')

        # assert
        self.assertEquals(result, ['expected'])
        mock_client.query.assert_called_with("DROP DATABASE data",
                                             database='data',
                                             epoch=None,
                                             chunked=False,
                                             chunk_size=0,
                                             method="POST")

    @mock.patch('lib.query.QueryAction.make_client')
    def test_run_chunked_override(self, mock_make_client):
        action = self.get_action_instance({})

        # mock
        mock_client = mock.MagicMock()
        mock_client.query.return_value = mock.MagicMock(raw='expected')
        mock_make_client.return_value = mock_client

        # run
        result = action.run(query="SELECT * FROM database",
                            chunked=99,
                            database='database',
                            epoch=None,
                            method=None)

        # assert
        self.assertEquals(result, ['expected'])
        mock_client.query.assert_called_with("SELECT * FROM database",
                                             database='database',
                                             epoch=None,
                                             chunked=True,
                                             chunk_size=99,
                                             method="GET")
