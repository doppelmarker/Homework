import json
import logging

from requests import exceptions, get

from rss_reader.reader._caching import NewsCache
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

    def start(self):
        try:
            self._setup()
            cache = NewsCache(self.config.cache_file_path, self.config.source)

            if self.config.cached:
                for news in cache.get_cached_news(
                    self.config.cached, self.config.source, self.config.limit
                ):
                    print(news)
                raise RestoredFromCache

            response = get(self.config.source, timeout=5)

            parser = Parser(response.text)

            dom = parser.parse()

            rss_builder = RSSBuilder(dom, self.config.limit)

            feed = rss_builder.build_feed()

            cache.cache_news(feed)

            if self.config.json:
                feed = feed.json()
                parsed_json = json.loads(feed)
                feed = json.dumps(parsed_json, indent=4)

            print(feed)

        except (exceptions.ConnectionError, exceptions.Timeout) as e:
            logger.warning("Connection problems")
            raise e
        except exceptions.RequestException as e:
            logger.warning("Invalid source URL")
            raise e
        except XMLError as e:
            logger.warning(e)
            raise e
