from typing import Dict, Type

from apps.parse.types import ParserType


class _AutoRegisterCatalogue(type):
    catalogue_map: Dict[str, Type["Catalogue"]] = {}

    def __init__(cls: Type["Catalogue"], cls_name, cls_bases, cls_dict):
        super().__init__(cls_name, cls_bases, cls_dict)
        if hasattr(cls, "name"):
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
    _parser_map: Dict[str, type] = {}

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
            # return parser
            # return type("SomeName", (parser,), attrs)

        return reg

    @classmethod
    def get_parser(cls, type_: str | ParserType) -> type:
        return cls._parser_map[type_]

    @staticmethod
    def get(name: str):
        return _AutoRegisterCatalogue.catalogue_map[name]

    @staticmethod
    def get_map():
        return _AutoRegisterCatalogue.catalogue_map

    @classmethod
    def get_names(cls) -> list:
        return list(_AutoRegisterCatalogue.catalogue_map.keys())

    @staticmethod
    def from_source(url: str):
        return [c for c in _AutoRegisterCatalogue.catalogue_map.values() if c.source == url][0]
