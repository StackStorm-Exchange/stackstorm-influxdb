from .base_action import BaseAction


class WriteAction(BaseAction):

    def run(self, points, points_raw, database, precision, retention_policy, **kwargs):
        client = self.make_client(**kwargs)

        if points_raw:
            # note: split also converts to a list, no matter what
            #       having the data in a list is SUPER important, otherwise
            #       write_points() screws up the input string, if only one line is pass in,
            #       by converting it into an array of characters instead of an
            #       array of a single string.
            points_raw_list = points_raw.split('\n')
            result = client.write_points(points_raw_list,
                                         time_precision=precision,
                                         database=database,
                                         retention_policy=retention_policy,
                                         protocol='line')
        else:
            result = client.write_points(points,
                                         time_precision=precision,
                                         database=database,
                                         retention_policy=retention_policy,
                                         protocol='json')
        return result
