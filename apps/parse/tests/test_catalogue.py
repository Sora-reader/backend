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


catalogue_names = Catalogue.get_names()


class CatalogueTestCase(TestCase):
    def test_every_catalogue_is_registered(self):
        self.assertEqual(len(catalogue_names), 2)

    @parametrize([dict(catalogue_name=name) for name in catalogue_names])
    def test_every_catalogue_at_least_1_parser(self, catalogue_name):
        self.assertTrue(Catalogue.get(catalogue_name).get_parser_map())

    @parametrize([dict(catalogue_name=name) for name in catalogue_names])
    def test_finds_list_parser(self, catalogue_name):
        self.assertTrue(Catalogue.get(catalogue_name).get_parser(ParserType.list))

    @parametrize([dict(catalogue_name=name) for name in catalogue_names])
    def test_finds_detail_parser(self, catalogue_name):
        self.assertTrue(Catalogue.get(catalogue_name).get_parser(ParserType.detail))

    # TODO: add tests for chapter_parser in mangachan after refactor
    # TODO: add tests for image_parser
