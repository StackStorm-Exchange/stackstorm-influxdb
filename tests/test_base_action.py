from influxdb_base_action_test_case import InfluxDBBaseActionTestCase
from influxdb import InfluxDBClient
from lib.base_action import BaseAction
from st2common.runners.base_action import Action


class TestActionLibBaseAction(InfluxDBBaseActionTestCase):
    __test__ = True
    action_cls = BaseAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)

    def test_resolve_credentials_no_config_credentials(self):
        action = self.get_action_instance({})
        action.config = {}
        result = action.resolve_credentials(test='kwargs')
        self.assertEquals(result, {'test': 'kwargs'})

    def test_resolve_credentials_default_credentials(self):
        action = self.get_action_instance({})
        action.config = {
            'credentials': {
                'default': {
                    'username': 'st2admin',
                    'password': 'secret',
                }
            }
        }
        result = action.resolve_credentials(test='kwargs')
        self.assertEquals(result, {'test': 'kwargs',
                                   'username': 'st2admin',
                                   'password': 'secret'})

    def test_resolve_credentials_non_exist_credentials_name(self):
        action = self.get_action_instance({})
        action.config = {
            'credentials': {
                'qa': {
                    'username': 'st2admin',
                    'password': 'secret',
                }
            }
        }
        with self.assertRaises(ValueError):
            action.resolve_credentials(credentials='doesnt_exist')

    def test_resolve_credentials_0no_kwargs_credentials_and_no_default_raises(self):
        action = self.get_action_instance({})
        action.config = {
            'credentials': {
                'qa': {
                    'username': 'st2admin',
                    'password': 'secret',
                }
            }
        }
        with self.assertRaises(ValueError):
            action.resolve_credentials(test='kwargs')

    def test_resolve_credentials_good_credentials(self):
        action = self.get_action_instance({})
        action.config = {
            'credentials': {
                'qa': {
                    'username': 'st2admin',
                    'password': 'secret',
                }
            }
        }
        result = action.resolve_credentials(credentials='qa', otherarg='othervalue')
        self.assertEquals(result, {
            'credentials': 'qa',
            'otherarg': 'othervalue',
            'username': 'st2admin',
            'password': 'secret',
        })

    def test_resolve_credentials_parameters_override_config(self):
        action = self.get_action_instance({})
        action.config = {
            'credentials': {
                'qa': {
                    'username': 'st2admin',
                    'password': 'secret',
                }
            }
        }
        result = action.resolve_credentials(credentials='qa',
                                            username='param_user')
        self.assertEquals(result, {
            'credentials': 'qa',
            'username': 'param_user',
            'password': 'secret',
        })

    def test_resolve_credentials_config_credentials_none_value(self):
        action = self.get_action_instance({})
        action.config = {
            'credentials': {
                'qa': {
                    'username': 'st2admin',
                    'password': None,
                }
            }
        }
        result = action.resolve_credentials(credentials='qa',
                                            username='param_user')
        self.assertEquals(result, {
            'credentials': 'qa',
            'username': 'param_user',
        })

    def test_resolve_config_no_kwargs(self):
        action = self.get_action_instance({})
        action.config = {'server': 'influxdb.domain.tld',
                         'ssl': True}
        result = action.resolve_config()
        self.assertEquals(result, {'server': 'influxdb.domain.tld',
                                   'ssl': True})

    def test_resolve_config_kwargs_override_config(self):
        action = self.get_action_instance({})
        action.config = {'ssl': True}
        result = action.resolve_config(ssl=False)
        self.assertEquals(result, {'ssl': False})

    def test_resolve_config_skip_credentials(self):
        action = self.get_action_instance({})
        action.config = {'username': 'st2admin',
                         'password': 'secret',
                         'credentials': 'default'}
        result = action.resolve_config()
        self.assertEquals(result, {})

    def test_resolve_config_none_values(self):
        action = self.get_action_instance({})
        action.config = {'server': None}
        result = action.resolve_config()
        self.assertEquals(result, {})

    def test_make_client(self):
        action = self.get_action_instance({})
        result = action.make_client(server='influxdb.domain.tld',
                                    port=8086,
                                    username='user',
                                    password='pass',
                                    ssl=True,
                                    verify_ssl=False)
        self.assertIsInstance(result, InfluxDBClient)
        self.assertEquals(result._host, 'influxdb.domain.tld')
        self.assertEquals(result._port, 8086)
        self.assertEquals(result._username, 'user')
        self.assertEquals(result._password, 'pass')
        self.assertEquals(result._scheme, 'https')
        self.assertEquals(result._verify_ssl, False)

    def test_ensure_list_given_non_list(self):
        action = self.get_action_instance({})
        result = action.ensure_list('abc')
        self.assertEquals(result, ['abc'])

    def test_ensure_list_given_list(self):
        action = self.get_action_instance({})
        data = [1]
        result = action.ensure_list(data)
        self.assertIs(result, data)

    def test_run(self):
        action = self.get_action_instance({})
        with self.assertRaises(NotImplementedError):
            action.run()
