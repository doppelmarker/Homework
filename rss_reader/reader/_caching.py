import json
import logging
from datetime import datetime

from rss_reader.rss_builder.rss_models import Feed, Item

logger = logging.getLogger("rss-reader")


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

    def cache_news(self, feed: Feed):
        if self.cache_file_path.is_file():
            with open(self.cache_file_path, "r+", encoding="utf-8") as cache_file:
                json_content = cache_file.read()

                cache_file.seek(0)

                try:
                    json_dict = json.loads(json_content) if json_content else dict()
                except json.decoder.JSONDecodeError:
                    logger.warning("Cache file is damaged! Clearing cache file...")
                    cache_file.truncate(0)
                    json_dict = dict()

                feed_head = feed.dict(exclude={"items"})
                if (
                    json_dict
                    and self.source in json_dict
                    and feed_head not in json_dict[self.source]
                ):
                    json_dict[self.source].append(feed_head)
                else:
                    json_dict[self.source] = list()
                    json_dict[self.source].append(feed_head)
                for item in feed.items:
                    if item.dict() not in json_dict[self.source]:
                        json_dict[self.source].append(item.dict())
                json.dump(json_dict, cache_file, indent=4, ensure_ascii=False)
        else:
            raise FileNotFoundError("Cache file not found")

    def get_cached_news(self, date, limit):
        if self.cache_file_path.is_file():
            with open(self.cache_file_path, "r", encoding="utf-8") as cache_file:
                if json_content := cache_file.read():
                    try:
                        json_dict = json.loads(json_content)
                    except json.decoder.JSONDecodeError:
                        logger.warning("Cache file is damaged! Clearing cache file...")
                        cache_file.truncate(0)
                        raise NewsNotFoundError(
                            "Cache file was damaged, that's why it was cleaned."
                        )

                    feeds = list()
                    items_count = 0

                    def get_feed_with_news_on_date(src):
                        nonlocal items_count

                        feed_head = json_dict[src][0]
                        items = list()
                        for item in json_dict[src][1:]:
                            datetime_obj = self._get_datetime_obj(item["pubDate"])
                            parsed_date = f"{datetime_obj.year}{datetime_obj.month:02d}{datetime_obj.day:02d}"
                            if parsed_date == date:
                                items.append(Item(**item))
                                items_count += 1
                                if items_count == limit:
                                    return Feed(**feed_head, items=items)
                        return Feed(**feed_head, items=items)

                    if self.source:
                        if self.source in json_dict.keys():
                            feeds.append(get_feed_with_news_on_date(self.source))
                    else:
                        for source in json_dict.keys():
                            feed = get_feed_with_news_on_date(source)
                            if feed.items:
                                feeds.append(feed)

                    if items_count == 0:
                        raise NewsNotFoundError(
                            f"No news found in cache for the specified date: {date}"
                        )

                    return feeds
                else:
                    raise NewsNotFoundError("Cache file is empty")
        else:
            raise FileNotFoundError("Cache file not found")
