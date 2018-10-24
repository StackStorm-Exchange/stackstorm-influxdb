# API docs
# https://docs.influxdata.com/influxdb/latest/tools/api
#
# Authentication docs
# https://docs.influxdata.com/influxdb/latest/administration/authentication_and_authorization/
from st2common.runners.base_action import Action
from influxdb import InfluxDBClient

import six

# options for login credentials in the config
CREDENTIALS_OPTIONS = [
    'credentials',
    'username',
    'password',
]


class BaseAction(Action):

    def resolve_credentials(self, **kwargs):
        """ Lookup credentials, by name, specified by the 'credentials' parameter
        during action invocation from the credentials dict stored in the config
        """
        # if there are no credentials specified in the config, we have nothing to lookup
        if not self.config.get('credentials'):
            return kwargs

        # get the name of credentials asked for during action invocation
        cred_name = kwargs.get('credentials')

        # if we couldn't find the 'credentials' from the parameters in the config
        # then try to use the default credential
        if not cred_name or cred_name not in self.config['credentials']:
            self.logger.debug('Credential [{}] is not in the config, trying [default]'
                              .format(cred_name))

            # if we couldn't find the default credential in the config (by name),
            # then raise an error
            cred_name = 'default'
            if cred_name not in self.config['credentials']:
                raise ValueError('Unable to find credentials [{}] or [default] in config'
                                 .format(kwargs.get('credentials')))

        # lookup the credential by name
        credentials = self.config['credentials'][cred_name]
        for k, v in six.iteritems(credentials):
            # skip if the user explicitly set this property during action invocation
            if kwargs.get(k) is not None:
                continue

            # only set the property if the value in the credential object is set
            if v is not None:
                kwargs[k] = v

        return kwargs

    def resolve_config(self, **kwargs):
        for k, v in six.iteritems(self.config):
            # skip if we're looking a `credentials` options
            if k in CREDENTIALS_OPTIONS:
                continue

            # skip if the user explicitly set this parameter when invoking the action
            if kwargs.get(k) is not None:
                continue

            # only set the property if the value is set in the config
            if v is not None:
                kwargs[k] = v

        return kwargs

    def make_client(self, **kwargs):
        kwargs = self.resolve_credentials(**kwargs)
        kwargs = self.resolve_config(**kwargs)
        return InfluxDBClient(host=kwargs['server'],
                              port=kwargs['port'],
                              username=kwargs['username'],
                              password=kwargs['password'],
                              ssl=kwargs['ssl'],
                              verify_ssl=kwargs['verify_ssl'])

    def ensure_list(self, d):
        if not isinstance(d, list):
            return [d]
        return d

    def run(self, **kwargs):
        raise NotImplementedError()
