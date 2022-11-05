from typing import Dict, Type

from django.core.cache import caches

from apps.parse.const import ParserType


class AutoRegisterCatalogue(type):
    _catalogue_map = {}

    def __init__(cls: Type["BaseCatalogue"], cls_name, cls_bases, cls_dict):
        if hasattr(cls, "name"):
            AutoRegisterCatalogue._catalogue_map[cls.name] = cls
        super().__init__(cls_name, cls_bases, cls_dict)


class BaseCatalogue(metaclass=AutoRegisterCatalogue):
    name: str
    source: str
    settings: str
    _parser_map: Dict[str, type] = {}

    @staticmethod
    def _create_init(cls):
        def _init(self, *args, **kwargs):
            url = kwargs.pop("url", None)
            if not getattr(self.__class__, "start_urls", None) and url:
                super(cls, self).__init__(*args, start_urls=[url])  # noqa
            else:
                super(cls, self).__init__(*args, **kwargs)

        return _init

    @classmethod
    def register(cls, type_: str | ParserType, cache: bool = True, url: bool = True):
        type_ = str(type_)

        def reg(parser: type):
            cls._parser_map[type_] = parser
            attrs = {
                "name": f"{cls.name}_{type_}",
                "type": type_,
            }
            if cache:
                attrs["cache"] = property(lambda self: caches[type_])
            if url:
                attrs["__init__"] = cls._create_init(parser)
            return type(parser.__name__, (parser,), attrs)

        return reg

    @classmethod
    def get_parser(cls, type_: str | ParserType) -> type:
        return cls._parser_map[str(type_)]

    @staticmethod
    def get_catalogue(name: str):
        return AutoRegisterCatalogue._catalogue_map[name]  # noqa
