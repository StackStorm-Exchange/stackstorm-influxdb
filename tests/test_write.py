from influxdb_base_action_test_case import InfluxDBBaseActionTestCase
from lib.base_action import BaseAction
from lib.write import WriteAction

import mock


class TestActionLibWriteAction(InfluxDBBaseActionTestCase):
    __test__ = True
    action_cls = WriteAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, WriteAction)
        self.assertIsInstance(action, BaseAction)

    @mock.patch('lib.write.WriteAction.make_client')
    def test_run_line_protocol(self, mock_make_client):
        action = self.get_action_instance({})

        # mock
        mock_client = mock.MagicMock()
        mock_client.write_points.return_value = 'expected'
        mock_make_client.return_value = mock_client

        points_raw = ('weather,location=us-midwest,season=summer temperature=82'
                      ' 1465839830100400200\n'
                      'weather,location=us-east,season=winter temperature=99'
                      ' 1465839830100400202')

        # run
        result = action.run(points=None,
                            points_raw=points_raw,
                            database='database',
                            precision='s',
                            retention_policy='FirstPolicy')

        # assert
        self.assertEquals(result, 'expected')
        points_list = ['weather,location=us-midwest,season=summer temperature=82'
                       ' 1465839830100400200',
                       'weather,location=us-east,season=winter temperature=99'
                       ' 1465839830100400202']
        mock_client.write_points.assert_called_with(points_list,
                                                    time_precision='s',
                                                    database='database',
                                                    retention_policy='FirstPolicy',
                                                    protocol='line')

    @mock.patch('lib.write.WriteAction.make_client')
    def test_run_json_protocol(self, mock_make_client):
        action = self.get_action_instance({})

        # mock
        mock_client = mock.MagicMock()
        mock_client.write_points.return_value = 'expected'
        mock_make_client.return_value = mock_client

        points = [
            {
                'measurement': 'weather',
                'tags': {
                    'location': 'us-midwest',
                    'season': 'summer',
                },
                'time': 1465839830100400200,
                'fields': {
                    'temperature': 82,
                }
            },
            {
                'measurement': 'weather',
                'tags': {
                    'location': 'us-east',
                    'season': 'winter',
                },
                'time': 1465839830100400202,
                'fields': {
                    'temperature': 99,
                }
            },
        ]

        # run
        result = action.run(points=points,
                            points_raw=None,
                            database='database',
                            precision='ns',
                            retention_policy='MyPolicy')

        # assert
        self.assertEquals(result, 'expected')
        mock_client.write_points.assert_called_with(points,
                                                    time_precision='ns',
                                                    database='database',
                                                    retention_policy='MyPolicy',
                                                    protocol='json')
