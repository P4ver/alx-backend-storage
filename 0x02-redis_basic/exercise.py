#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(func: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.'''
    @wraps(func)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.'''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(func.__qualname__)
        return func(self, *args, **kwargs)
    return invoker


def call_history(func: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.'''
    @wraps(func)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.'''
        inputs_key = '{}:inputs'.format(func.__qualname__)
        outputs_key = '{}:outputs'.format(func.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs_key, str(args))
        result = func(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outputs_key, result)
        return result
    return invoker


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.'''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_instance = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_instance, redis.Redis):
        return
    func_name = fn.__qualname__
    inputs_key = '{}:inputs'.format(func_name)
    outputs_key = '{}:outputs'.format(func_name)
    call_count = 0
    if redis_instance.exists(func_name) != 0:
        call_count = int(redis_instance.get(func_name))
    print('{} was called {} times:'.format(func_name, call_count))
    inputs_list = redis_instance.lrange(inputs_key, 0, -1)
    outputs_list = redis_instance.lrange(outputs_key, 0, -1)
    for input_data, output_data in zip(inputs_list, outputs_list):
        print('{}(*{}) -> {}'.format(
            func_name,
            input_data.decode("utf-8"),
            output_data,
        ))


class Cache:
    '''Represents an object for storing data in a Redis data storage.'''
    def __init__(self) -> None:
        '''Initializes a Cache instance.'''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in a Redis data storage and returns the key.'''
        unique_key = str(uuid.uuid4())
        self._redis.set(unique_key, data)
        return unique_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from a Redis data storage.'''
        value = self._redis.get(key)
        return fn(value) if fn is not None else value

    def get_str(self, key: str) -> str:
        '''Retrieves a string value from a Redis data storage.'''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from a Redis data storage.'''
        return self.get(key, lambda x: int(x))
