#!/usr/bin/env python3
""" Redis module. """

from functools import wraps
import redis
import sys
from typing import Union, Optional, Callable
from uuid import uuid4


def replay(func: Callable):
    """ Replay. """
    func_name = func.__qualname__
    inputs_key = "".join([func_name, ":inputs"])
    outputs_key = "".join([func_name, ":outputs"])
    call_count = func.__self__.get(func_name)
    inputs_list = func.__self__._redis.lrange(inputs_key, 0, -1)
    outputs_list = func.__self__._redis.lrange(outputs_key, 0, -1)
    history = list(zip(inputs_list, outputs_list))
    print(f"{func_name} was called {decode_utf8(call_count)} times:")
    for input_val, output_val in history:
        input_val = decode_utf8(input_val)
        output_val = decode_utf8(output_val)
        print(f"{func_name}(*{input_val}) -> {output_val}")


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def count_calls(func: Callable) -> Callable:
    """ Count calls """
    func_name = func.__qualname__

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """ Wrapper """
        self._redis.incr(func_name)
        return func(self, *args, **kwargs)
    return wrapper


def decode_utf8(bt: bytes) -> str:
    """ decodes, """
    return bt.decode('utf-8') if isinstance(bt, bytes) else byte_data


class Cache:
    """ cache class, """

    def __init__(self):
        """ Init """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Random to store """
        unique_key = str(uuid4())
        self._redis.set(unique_key, data)
        return unique_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                    bytes,
                                                                    int,
                                                                    float]:
        """ Gets """
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, byte_data: bytes) -> str:
        """ Bytes to string """
        return byte_data.decode('utf-8')

    def get_int(self, byte_data: bytes) -> int:
        """ Bytes to integer """
        return int.from_bytes(byte_data, sys.byteorder)
