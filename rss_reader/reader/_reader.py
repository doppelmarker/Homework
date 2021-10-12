import logging
from html import unescape

from requests import exceptions, get

from rss_reader.convert import Converter
from rss_reader.printer import NewsPrinter
from rss_reader.reader import NewsCache
from rss_reader.rss_builder import RSSBuilder
from rss_reader.xml_parser import Parser
from rss_reader.xml_parser.tokenizer import XMLError

logger = logging.getLogger("rss-reader")


class RestoredFromCache(Exception):
    pass


class Reader:
    def __init__(self, config):
        self.config = config

    def _setup(self):
        if self.config.verbose:
            formatter = logging.Formatter(
                "[%(levelname)s] %(asctime)s (%(funcName)s) = %(message)s"
            )
            logger_ = logging.getLogger("rss-reader")
            logger_.setLevel("DEBUG")
            s_handler = logging.StreamHandler()
            s_handler.setFormatter(formatter)
            logger_.addHandler(s_handler)
            logger_.info("Enabled verbose mode")
        else:
            logger.addHandler(logging.NullHandler())
            logger.propagate = False

    def _get_cached(self, cache):
        return cache.get_cached_news(self.config.cached, self.config.limit)

    def _get_parsed(self, cache):
        try:
            rss_webpage = get(self.config.source, timeout=5)

            parser = Parser(unescape(rss_webpage.text))

            dom = parser.parse()

            rss_builder = RSSBuilder(dom, self.config.limit)

            feed = rss_builder.build_feed()

            cache.cache_news(feed)

            return feed
        except (exceptions.ConnectionError, exceptions.Timeout) as e:
            logger.warning("Connection problems")
            raise e
        except exceptions.RequestException as e:
            logger.warning("Invalid source URL")
            raise e
        except XMLError as e:
            logger.warning(e)
            raise e

    def start(self):
        self._setup()

        cache = NewsCache(self.config.cache_file_path, self.config.source)

        feeds = []

        if self.config.cached:
            feeds.extend(self._get_cached(cache))
        else:
            feeds.append(self._get_parsed(cache))

        converter = Converter(self.config.format) if self.config.format else None

        printer = NewsPrinter(converter, self.config.json)

        printer.print(feeds)

        if self.config.cached:
            raise RestoredFromCache
