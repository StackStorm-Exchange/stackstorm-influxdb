from base_action import BaseAction


class PingAction(BaseAction):

    def run(self, **kwargs):
        client = self.make_client(**kwargs)
        return client.ping()
