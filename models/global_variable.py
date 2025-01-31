from cachetools import TTLCache, cached

cache = TTLCache(maxsize=128, ttl=604800)
