"""Module containing the core logics. The place from where the program's logic gets branched."""
import logging
from html import unescape
from typing import List

from requests import exceptions, get

from rss_reader.config import Config
from rss_reader.converter import Converter
from rss_reader.printer import NewsPrinter
from rss_reader.reader import NewsCache
from rss_reader.rss_builder import Feed, RSSBuilder
from rss_reader.xml_parser import Parser, XMLError

logger = logging.getLogger("rss-reader")


class NotRSSError(Exception):
    """Raised whenever the link given in source argument leads not to XML page."""


class Reader:
    """Entry class encompassing the core application logics."""

    # valid RSS mime_types
    rss_mime_types = {
        "application/xml",
        "application/rss+xml",
        "text/xml",
    }

    def __init__(self, config: Config):
        self.config = config

    @staticmethod
    def _is_rss(grabbed):
        """Method defining whether grabbed content represents RSS channel."""
        for rss_mime_type in Reader.rss_mime_types:
            if rss_mime_type in grabbed.headers["content-type"]:
                return True
        return False

    def _get_cached(self, cache: NewsCache) -> List[Feed]:
        """Private method to obtain the list of cached feeds."""
        return cache.get_cached_news(self.config.cached, self.config.limit)

    def _get_parsed(self, cache: NewsCache) -> Feed:
        """Private method to obtain a parsed feed."""
        try:
            grabbed = get(self.config.source, timeout=5)

            if not self._is_rss(grabbed):
                raise NotRSSError(f"{self.config.source} is not RSS!")

            parser = Parser(unescape(grabbed.text))

            dom = parser.parse()

            rss_builder = RSSBuilder(dom, self.config.limit, self.config.check_urls)

            feed = rss_builder.build_feed()

            cache.cache_news(feed)

            return feed
        except (exceptions.ConnectionError, exceptions.Timeout) as e:
            logger.error("Connection problems!")
            raise e
        except exceptions.RequestException as e:
            logger.error(f"Invalid source URL: {self.config.source}!")
            raise e
        except XMLError as e:
            logger.error(e)
            raise e
        except NotRSSError as e:
            logger.error(e)
            raise e

    def start(self):
        """Public method to start the core application logics."""
        cache = NewsCache(self.config.cache_file_path, self.config.source)

        feeds = []

        if self.config.cached:
            feeds.extend(self._get_cached(cache))
            logger.info("Restored data from cache.")
        else:
            feeds.append(self._get_parsed(cache))

        printer = NewsPrinter(self.config.json, self.config.colorize)

        printer.print(feeds)

        converter = Converter(self.config.format) if self.config.format else None

        if converter:
            converter.convert(feeds)
