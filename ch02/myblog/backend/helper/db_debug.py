from django.db import connection
from django.db import reset_queries


def database_debug(func):
    def inner_func(*args, **kwargs):
        reset_queries()
        results = func(*args, **kwargs)
        query_info = connection.queries
        print(f"function_name: {func.__name__}")
        print(f"query_count: {len(query_info)}")
        queries = [f"{query['sql']}\n" for query in query_info]
        print(f"queries: \n{''.join(queries)}")
        return results

    return inner_func
