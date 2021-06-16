# Create your tests here.
from django.test import TestCase

from apps.parse.management.commands.parse_readmanga import Command
from apps.parse.models import Manga


class ParseTestCase(TestCase):
    def test_parsing(self):
        Command().handle()
        manga_descriptions = Manga.objects.values_list("title", "description")
        for title, description in manga_descriptions:
            print(title, description)
