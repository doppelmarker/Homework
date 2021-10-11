import codecs
import json
from datetime import datetime

from rss_reader.rss_builder.rss_models import Item


class NewsNotFoundError(Exception):
    pass


class NewsCache:
    valid_date_formats = [
        # RFC 822 date format (standard for RSS)
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%SZ",
    ]

    def __init__(self, cache_file_path, source):
        self.cache_file_path = cache_file_path
        self.source = source

    @staticmethod
    def _get_datetime_obj(date_string):
        for date_format in NewsCache.valid_date_formats:
            try:
                return datetime.strptime(date_string, date_format)
            except ValueError:
                pass
        raise ValueError(
            f"{date_string!r} is not in a valid format! valid formats: {NewsCache.valid_date_formats}"
        )

    def cache_news(self, feed):
        if self.cache_file_path.is_file():
            with open(self.cache_file_path, "r+", encoding="utf-8") as cache_file:
                json_content = cache_file.read()
                json_dict = json.loads(json_content) if json_content else dict()
                cache_file.seek(0)
                for item in feed.items:
                    if (
                        json_dict
                        and self.source in json_dict
                        and item.dict() not in json_dict[self.source]
                    ):
                        json_dict[self.source].append(item.dict())
                    else:
                        json_dict[self.source] = list()
                        json_dict[self.source].append(item.dict())
                json.dump(json_dict, cache_file, indent=4, ensure_ascii=False)
        else:
            raise FileNotFoundError("Cache file not found")

    def get_cached_news(self, date, limit):
        if self.cache_file_path.is_file():
            with open(self.cache_file_path, "r") as cache_file:
                if json_content := cache_file.read():
                    json_dict = json.loads(json_content)

                    items = list()

                    class LimitAchieved(Exception):
                        """Helper exception to determine whether the limit of news is achieved."""

                    def append_items(src):
                        for item in json_dict[src]:
                            datetime_obj = self._get_datetime_obj(item["pubDate"])
                            parsed_date = f"{datetime_obj.year}{datetime_obj.month:02d}{datetime_obj.day:02d}"
                            if parsed_date == date:
                                items.append(Item(**item))
                                if len(items) == limit:
                                    raise LimitAchieved

                    try:
                        if self.source:
                            if self.source in json_dict.keys():
                                append_items(self.source)
                        else:
                            for source in json_dict.keys():
                                append_items(source)
                    except LimitAchieved:
                        return items

                    if len(items) == 0:
                        raise NewsNotFoundError(
                            f"No news found in cache for the specified date: {date}"
                        )

                    return items
                else:
                    raise NewsNotFoundError("Cache file is empty")
        else:
            raise FileNotFoundError("Cache file not found")
