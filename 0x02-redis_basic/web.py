#!/usr/bin/env python3
'''A module with tools for caching HTTP requests and tracking request counts.
'''
import redis
import requests
from functools import wraps
from typing import Callable


cache_instance = redis.Redis()
'''The module-level Redis instance.
'''


def cache_data(func: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(func)
    def wrapper(url: str) -> str:
        '''The wrapper function for caching the output.
        '''
        cache_instance.incr(f'count:{url}')
        cached_result = cache_instance.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')
        result = func(url)
        cache_instance.set(f'count:{url}', 0)
        cache_instance.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_data
def fetch_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request count.
    '''
    return requests.get(url).text
