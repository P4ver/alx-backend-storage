#!/usr/bin/env python3
"""
Web file
"""
import requests
import redis
from functools import wraps

cache_instance = redis.Redis()


def track_url_access(func):
    """ Decorator counting how many times
    a URL is accessed """
    @wraps(func)
    def wrapper(url):
        cache_key = "cached:" + url
        cached_content = cache_instance.get(cache_key)
        if cached_content:
            return cached_content.decode("utf-8")

        access_count_key = "count:" + url
        html_content = func(url)

        cache_instance.incr(access_count_key)
        cache_instance.set(cache_key, html_content)
        cache_instance.expire(cache_key, 10)
        return html_content
    return wrapper


@track_url_access
def fetch_page(url: str) -> str:
    """ Returns HTML content of a URL """
    response = requests.get(url)
    return response.text
