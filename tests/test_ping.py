from influxdb_base_action_test_case import InfluxDBBaseActionTestCase
from lib.base_action import BaseAction
from lib.ping import PingAction

import mock


class TestActionLibPingAction(InfluxDBBaseActionTestCase):
    __test__ = True
    action_cls = PingAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, PingAction)
        self.assertIsInstance(action, BaseAction)

    @mock.patch('lib.ping.PingAction.make_client')
    def test_run(self, mock_make_client):
        action = self.get_action_instance({})

        # mock
        mock_client = mock.MagicMock()
        mock_client.ping.return_value = 'expected'
        mock_make_client.return_value = mock_client

        # run
        result = action.run()

        # assert
        self.assertEquals(result, 'expected')
