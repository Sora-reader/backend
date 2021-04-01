import datetime as dt

import pytz
from django.core.management.base import BaseCommand

from apps.readmanga_parser.models import Manga
from apps.readmanga_parser.parser.lxml_parser.detail_parse import get_detailed_info, save_detailed_manga_info


class Command(BaseCommand):
    help = "Detailed parsing"

    def handle(self, *args, **options):
        manga = Manga.objects.get(name__icontains="Поднятие уровня в одиночку")
        url = manga.self_url
        if detailed := manga.technical_params.get('time_detailed'):
            detailed = dt.datetime.strptime(detailed, '%Y-%m-%d %H:%M:%S')
            detailed.tzinfo = pytz.UTC
            update_deadline = detailed - dt.timedelta(minutes=30)
            if dt.datetime.now(pytz.UTC) > update_deadline:
                return

        info: dict = get_detailed_info(url)
        save_detailed_manga_info(**info)
