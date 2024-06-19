#!/usr/bin/env python3
"""
Web file module
"""

import requests
import redis
from functools import wraps
from typing import Callable

cache_instance = redis.Redis()
"""The module-level Redis instance for caching and tracking URL access."""


def track_url_access(func: Callable[[str], str]) -> Callable[[str], str]:
    """Decorator that counts how many times a URL
    is accessed and caches the result.

    Args:
        func (Callable[[str], str]): The function to wrap.

    Returns:
        Callable[[str], str]: The wrapped function.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """Wrapper function for caching the output and counting accesses.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL.
        """
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
    """Fetches and returns the HTML content of a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
