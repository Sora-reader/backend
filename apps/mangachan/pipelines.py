from copy import deepcopy

from apps.readmanga.pipelines import ReadmangaChapterPipeline, ReadmangaPipeline


class MangachanChapterPipeline(ReadmangaChapterPipeline):
    pass


class MangachanPipeline(ReadmangaPipeline):
    def process_item(self, data, spider):
        item = deepcopy(data)
        chapters = item.pop("chapters")
        super().process_item(item, spider)
        return chapters
