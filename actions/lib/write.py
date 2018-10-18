from base_action import BaseAction


class WriteAction(BaseAction):

    def run(self, points, points_raw, database, precision, retention_policy, **kwargs):
        client = self.make_client(**kwargs)

        if points_raw:
            data = points_raw
            protocol = 'line'
        else:
            data = points
            protocol = 'json'
        return client.write_points(data,
                                   time_precision=precision,
                                   database=database,
                                   retention_policy=retention_policy,
                                   protocol=protocol)
