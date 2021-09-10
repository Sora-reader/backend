from copy import deepcopy

from apps.parse.manga_chan.list_parser.manga_spider import MangaChanSpider
from apps.parse.models import Genre, Manga
from apps.parse.readmanga.list_parser.pipelines import bulk_get_or_create


class MangaChanPipeline:
    @staticmethod
    def process_item(item, spider: "MangaChanSpider"):
        data = deepcopy(item)
        title = data.pop("title")
        genres = data.pop("genres")
        source_url = data.pop("source_url")

        if not title:
            message = f"Error processing {data}: No title name was set"
            spider.logger.error(message)
            raise KeyError(message)

        genres = bulk_get_or_create(Genre, genres)

        manga, _ = Manga.objects.get_or_create(source_url=source_url)
        manga: Manga

        manga_already = Manga.objects.filter(source_url=source_url)
        if manga_already.exists():
            manga_already.update(title=title, **data)
            manga = manga_already.first()
            spider.logger.info(f'Updated item "{manga}"')
        else:
            manga = Manga.objects.create(
                title=title,
                source_url=source_url,
                **data,
            )
            spider.logger.info(f'Created item "{manga}"')

        manga.genres.add(*genres)

        return item
