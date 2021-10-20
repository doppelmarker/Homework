"""
Module providing caching functionality.
Cache is stored in a json file.
For the structure and more detailed info regarding cache, please, refer to the README.txt file.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from rss_reader.rss_builder import Feed, Item

logger = logging.getLogger("rss-reader")


class NewsNotFoundError(Exception):
    """Raised whenever news was not found in cache file."""

    pass


class NewsCache:
    """
    Class providing 2 public methods: cache_news and get_cached_news. Because caching works every time after getting
    and parsing an XML page, its instance's method cache_news is called every time the program runs. Whenever --date
    argument with a date in the format '20211020' is provided, the news specified by this date is returned from cache
    file as a list of feeds because different feeds may have news published on the same date. Due to the fact that in
    different RSS channels items may have different format of <pubDate> tag, it may be hard to programmatically
    convert its time value to our format in order to perform comparison, that's why there is a class field
    valid_date_formats, which defines legit date formats the application can distinguish. Whenever --date arguments
    is provided both with source argument, then the news published on the given date within this source are returned
    are returned from cache (if there are some).
    """

    valid_date_formats = {
        # RFC 822 date format (standard for RSS)
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%SZ",
    }

    def __init__(self, cache_file_path: Path, source: Optional[str]):
        self.cache_file_path = cache_file_path
        self.source = source

    @staticmethod
    def _get_datetime_obj(date_string: str) -> datetime:
        """Private method to obtain a datetime object for the item's <pubDate> tag."""
        for date_format in NewsCache.valid_date_formats:
            try:
                return datetime.strptime(date_string, date_format)
            except ValueError:
                pass
        raise ValueError(
            f"{date_string!r} is not in a valid format! Valid formats: {NewsCache.valid_date_formats}"
        )

    def cache_news(self, feed: Feed) -> None:
        """Public method to perform caching. If cache file was somehow damaged, it gets cleaned without crashing the
        application."""
        if self.cache_file_path.is_file():
            with open(self.cache_file_path, "r+", encoding="utf-8") as cache_file:
                json_content = cache_file.read()

                cache_file.seek(0)

                try:
                    json_dict = json.loads(json_content) if json_content else dict()
                except json.decoder.JSONDecodeError:
                    logger.warning("Cache file is damaged! Cleaning cache file...")
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
            raise FileNotFoundError("Cache file was not found!")

    def get_cached_news(self, date: str, limit: int) -> List[Feed]:
        """
        Public method to obtain a list of feeds which contain news published on date equal to the provided one in
        --date argument.\n
        For example, if in cache file there are 2 feeds, the first of which contains 3 news and the
        second one contains 2 news, all published on the same date, this date is equal to one passed in --date
        argument, whereas --limit argument's value is equal to 4, then the resulting feeds list will contain the
        whole first feed with 3 news from cache and the second feed but only with 1 news.
        """
        if self.cache_file_path.is_file():
            with open(self.cache_file_path, "r", encoding="utf-8") as cache_file:
                if json_content := cache_file.read():
                    try:
                        json_dict = json.loads(json_content)
                    except json.decoder.JSONDecodeError:
                        logger.warning("Cache file is damaged! Cleaning cache file...")
                        cache_file.truncate(0)
                        raise NewsNotFoundError(
                            "Cache file was damaged, that's why it was cleaned."
                        )

                    feeds = list()
                    items_count = 0

                    def get_feed_with_news_on_date(src: str) -> Feed:
                        """Enclosed function to fill the list of feeds with feeds containing news published on the
                        given date. Returns a feed."""
                        # items_count is used to keep track of how many items were already found with the given
                        # pubDate in order to satisfy --limit argument
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
                            raise NewsNotFoundError(
                                f"No news specified by the RSS {self.source} was found in cache!"
                            )
                    else:
                        for source in json_dict.keys():
                            feed = get_feed_with_news_on_date(source)
                            if feed.items:
                                feeds.append(feed)

                    if items_count == 0:
                        no_news_msg = (
                            f"No news published on {date} specified by the RSS {self.source} was found in cache!"
                            if self.source
                            else f"No news published on {date} was found in cache!"
                        )
                        raise NewsNotFoundError(no_news_msg)
                    return feeds
                else:
                    raise NewsNotFoundError("Cache file is empty!")
        else:
            raise FileNotFoundError("Cache file was not found!")
