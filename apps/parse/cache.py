from django.core.cache import caches


class CacheConnector:
    cache_key: str

    @property
    def cache(self):
        return caches[self.cache_key]


class WithCache:
    def __call__(self, cache_key: str):
        return type("CacheConnector", (CacheConnector,), {"cache_key": cache_key})
