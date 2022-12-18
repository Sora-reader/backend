from abc import ABC, abstractmethod
from typing import Any

from django.core.cache import caches

from apps.parse.types import CacheType


class BasePipeline:
    pass


class CachedPipeline(BasePipeline, ABC):
    timeout = 0
    convert = True
    type: str

    @abstractmethod
    def get_cache_key(self, data) -> str:
        ...

    @abstractmethod
    def process(self, item, spider) -> Any:
        return

    def convert_data(self, data) -> Any:
        ...

    def process_item(self, item, spider) -> Any:
        res = self.process(item, spider)
        self.save_to_cache(item, spider)
        return res

    def save_to_cache(self, data, spider):
        """Save item to cache."""
        spider.logger.info("Saving data to cache")

        key = self.get_cache_key(data)
        if self.__class__.convert:
            data = self.convert_data(data)

        cache = caches[CacheType.from_parser_type(self.__class__.type)]
        cache.set(key, data, timeout=self.__class__.timeout)


class ChapterPipeline(CachedPipeline, ABC):
    pass
