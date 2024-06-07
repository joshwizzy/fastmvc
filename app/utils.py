import cachetools
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)


def cache_response(key, value):
    cache[key] = value


def get_cached_response(key):
    return cache.get(key)


def clear_cache(key):
    if key in cache:
        del cache[key]
