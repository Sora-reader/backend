from django.core.management.base import BaseCommand

from apps.readmanga_parser.parser.lxml_parser.detail_parse import get_detailed_info, save_detailed_manga_info


class Command(BaseCommand):
    help = "Detailed parsing"

    def handle(self, *args, **options):
        url = "https://readmanga.live/seven_days"
        info: dict = get_detailed_info(url)
        save_detailed_manga_info(**info)
