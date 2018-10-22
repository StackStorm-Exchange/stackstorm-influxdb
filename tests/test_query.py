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

    # @mock.patch('lib.ping.PingAction.make_client')
    # def test_run(self, mock_make_client):
    #     action = self.get_action_instance({})

    #     # mock
    #     mock_client = mock.MagicMock()
    #     mock_client.ping.return_value = 'expected'
    #     mock_make_client.return_value = mock_client

    #     # run
    #     result = action.run()

    #     # assert
    #     self.assertEquals(result, 'expected')
