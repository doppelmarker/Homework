import json
import logging

from requests import exceptions, get

from rss_reader.rss_builder import RSSBuilder
from rss_reader.xml_parser import Parser

logger = logging.getLogger("rss-reader")


class Reader:
    def __init__(self, config):
        self.config = config

    def _get_xml(self):
        try:
            response = get(self.config.source, timeout=5)
            return response.text
        except (exceptions.ConnectionError, exceptions.Timeout) as e:
            logger.warning("Connection problems")
            raise e
        except exceptions.RequestException as e:
            logger.warning("Invalid source URL")
            raise e

    def start(self):
        parser = Parser(self._get_xml())

        dom = parser.parse()

        rss_builder = RSSBuilder(dom, self.config.limit)

        feed = rss_builder.build_feed()

        if self.config.json:
            feed = feed.json()
            parsed_json = json.loads(feed)
            feed = json.dumps(parsed_json, indent=4)

        print(feed)
