from typing import Dict, Type

from apps.parse.exceptions import CatalogueNotFound, ParserNotFound
from apps.parse.types import ParserType


class _AutoRegisterCatalogue(type):
    catalogue_map: Dict[str, Type["Catalogue"]] = {}

    def __init__(cls: Type["Catalogue"], cls_name, cls_bases, cls_dict):
        super().__init__(cls_name, cls_bases, cls_dict)
        # Applies to every catalogue, but not base Catalogue class
        if hasattr(cls, "name"):
            # Create parser map for catalogue
            cls._parser_map = {}
            _AutoRegisterCatalogue.catalogue_map[cls.name] = cls

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
    _parser_map: Dict[str, type]

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
        def reg(parser: type):
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

    @classmethod
    def get_parser(cls, type_: str | ParserType) -> type:
        res = cls._parser_map.get(type_, None)
        if not res:
            raise ParserNotFound
        return res

    @classmethod
    def get_parser_map(cls) -> dict:
        return cls._parser_map

    @staticmethod
    def get(name: str):
        res = _AutoRegisterCatalogue.catalogue_map.get(name, None)
        if not res:
            raise CatalogueNotFound
        return res

    @staticmethod
    def get_map():
        return _AutoRegisterCatalogue.catalogue_map

    @classmethod
    def get_names(cls) -> list:
        return list(_AutoRegisterCatalogue.catalogue_map.keys())

    @classmethod
    def get_sources(cls) -> list:
        return [c.source for c in _AutoRegisterCatalogue.catalogue_map.values()]

    @staticmethod
    def from_source(url: str):
        filtered_list = [
            c for c in _AutoRegisterCatalogue.catalogue_map.values() if c.source == url
        ]
        if not filtered_list:
            raise CatalogueNotFound
        return filtered_list[0]

    @classmethod
    def source_to_catalogue_name_map(cls):
        return {c.source: c.name for c in cls.get_map().values()}
