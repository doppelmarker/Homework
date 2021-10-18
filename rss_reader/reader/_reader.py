import logging
from html import unescape

from requests import exceptions, get

from rss_reader.converter import Converter
from rss_reader.printer import NewsPrinter
from rss_reader.reader import NewsCache
from rss_reader.rss_builder import RSSBuilder
from rss_reader.xml_parser import Parser
from rss_reader.xml_parser.tokenizer import XMLError

logger = logging.getLogger("rss-reader")


class NotRSSError(Exception):
    pass


class Reader:
    def __init__(self, config):
        self.config = config

    def _get_cached(self, cache):
        return cache.get_cached_news(self.config.cached, self.config.limit)

    def _get_parsed(self, cache):
        try:
            rss_webpage = get(self.config.source, timeout=5)

            if "application/xml" not in rss_webpage.headers["content-type"]:
                raise NotRSSError(f"{self.config.source} is not RSS!")

            parser = Parser(unescape(rss_webpage.text))

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
