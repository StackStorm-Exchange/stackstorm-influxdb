from base_action import BaseAction


class QueryAction(BaseAction):

    def detect_query_method(self, query):
        """
        GET - Use for all queries that start with: SELECT, SHOW
              The only exceptions are SELECT queries that include an INTO clause.
              Those SELECT queries require a POST request.
        POST - Use for all queries taht start with:
               ALTER, CREATE, DELETE, DROP, GRANT, KILL, REVOKE
        """
        query_lower = query.lower()
        method = None
        if query_lower.startswith("select "):
            method = "GET"
            if " into " in query_lower:
                method = "POST"
        elif query_lower.startswith("show "):
            method = "GET"
        # test for a list of strings that it may start with. do this using a tuple
        # https://stackoverflow.com/questions/20461847/str-startswith-with-a-list-of-strings-to-test-for
        elif quuery_lower.startswith(tuple(["alter ",
                                            "create ",
                                            "delete ",
                                            "drop ",
                                            "grant ",
                                            "kill ",
                                            "revoke "])):
            method = "POST"
        else:
            raise ValueError("Couldn't auto-detect the method for the query: {}".format(query))

        return method

    def run(self, query, chunked, database, epoch, method, **kwargs):
        client = self.make_client(**kwargs)

        # chunked
        is_chunked = (chunked > 0)
        chunked_size = chunked

        # method
        if not method:
            method = self.detect_query_method(query)

        # execute query
        result_set = client.query(kwargs['query'],
                                  database=database,
                                  epoch=kwargs['epoch'],
                                  chunked=is_chunked,
                                  chunked_size=chunked_size,
                                  method=method)
        result_set = self.ensure_list(result_set)

        # return the "raw" JSON/dict from each ResultSet object
        return [r.raw() for r in result_set]
