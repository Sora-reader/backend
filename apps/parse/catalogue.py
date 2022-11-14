from typing import Dict, List, Type

from django.utils.functional import classproperty

from apps.parse.exceptions import CatalogueNotFound, ParserNotFound
from apps.parse.scrapy.spider import BaseSpider
from apps.parse.types import ParserType


class CatalogueMap(dict, Dict[str, Type["Catalogue"]]):
    @property
    def names(self) -> List[str]:
        return [c.name for c in self.values()]

    @property
    def sources(self) -> List[str]:
        return [c.source for c in self.values()]

    @property
    def name_to_source_map(self) -> Dict[str, str]:
        return {c.name: c.source for c in self.values()}

    @property
    def source_to_name_map(self) -> Dict[str, str]:
        return {c.source: c.name for c in self.values()}


class _AutoRegisterCatalogue(type):
    catalogue_map = CatalogueMap()

    def __init__(cls: Type["Catalogue"], cls_name, cls_bases, cls_dict):
        super().__init__(cls_name, cls_bases, cls_dict)
        # Applies to every catalogue, but not base Catalogue class
        if hasattr(cls, "name"):
            # Create parser map for catalogue
            cls._parser_map = {}
            _AutoRegisterCatalogue.catalogue_map[cls.name] = cls

    def get_map(cls):
        return cls.catalogue_map

    def __str__(cls: Type["Catalogue"]):
        return cls.name

    def __hash__(cls: Type["Catalogue"]):
        return hash(cls.name)

    def __eq__(cls: Type["Catalogue"], other):
        if type(other) == str:
            return cls.name == other
        return super().__eq__(other)


class Catalogue(metaclass=_AutoRegisterCatalogue):
    name: str
    source: str
    settings: str
    _parser_map: Dict[str, Type["BaseSpider"]]

    @staticmethod
    def _create_init(cls):
        original_init = cls.__init__

        def _init(self, *args, **kwargs):
            url = kwargs.pop("url", None)
            if not getattr(self.__class__, "start_urls", None) and url:
                original_init(self, *args, start_urls=[url])  # noqa
            else:
                original_init(self, *args, **kwargs)

        return _init

    @classmethod
    def register(cls, type_: str | ParserType, url: bool = True):
        def reg(parser: Type["BaseSpider"]):
            cls._parser_map[type_] = parser
            attrs = {
                "name": f"{cls.name}_{type_}",
                "type": type_,
            }
            if url:
                parser.__init__ = cls._create_init(parser)
                attrs["__init__"] = cls._create_init(parser)

            parser.name = attrs["name"]
            parser.type = attrs["type"]

        return reg

    @staticmethod
    def from_name(name: str):
        res = _AutoRegisterCatalogue.catalogue_map.get(name, None)
        if not res:
            raise CatalogueNotFound
        return res

    @staticmethod
    def from_source(url: str):
        filtered_list = [
            c for c in _AutoRegisterCatalogue.catalogue_map.values() if c.source == url
        ]
        if not filtered_list:
            raise CatalogueNotFound
        return filtered_list[0]

    @classproperty
    def map(self):
        return _AutoRegisterCatalogue.catalogue_map

    @classmethod
    def from_parser_name(cls, type_: str | ParserType):
        res = cls._parser_map.get(type_, None)
        if not res:
            raise ParserNotFound
        return res

    @classproperty
    def parser_map(self):
        return self._parser_map
