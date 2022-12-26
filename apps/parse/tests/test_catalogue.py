import functools

from django.test import TestCase

from apps.parse.catalogue import Catalogue
from apps.parse.types import ParserType


def parametrize(param_list):
    """Decorates a test case to run it as a set of subtests."""

    def decorator(f):
        @functools.wraps(f)
        def wrapped(self):
            for param in param_list:
                with self.subTest(**param):
                    f(self, **param)

        return wrapped

    return decorator


catalogue_names = Catalogue.map.names


class CatalogueTestCase(TestCase):
    def test_every_catalogue_is_registered(self):
        self.assertEqual(len(catalogue_names), 2)

    @parametrize([dict(catalogue_name=name) for name in catalogue_names])
    def test_every_catalogue_at_least_1_parser(self, catalogue_name):
        self.assertTrue(Catalogue.from_name(catalogue_name).parser_map)

    @parametrize([dict(catalogue_name=name) for name in catalogue_names])
    def test_finds_list_parser(self, catalogue_name):
        self.assertTrue(Catalogue.from_name(catalogue_name).from_parser_name(ParserType.list))

    @parametrize([dict(catalogue_name=name) for name in catalogue_names])
    def test_finds_detail_parser(self, catalogue_name):
        self.assertTrue(Catalogue.from_name(catalogue_name).from_parser_name(ParserType.detail))

    # TODO: add tests for chapter_parser in mangachan after refactor
    # TODO: add tests for image_parser
