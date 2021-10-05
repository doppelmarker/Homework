import json

import requests

from rss_reader.rss_builder import RSSBuilder
from rss_reader.xml_parser import Parser


class Reader:
    def __init__(self, config):
        self.config = config

    def start(self):
        response = requests.get(self.config.source)

        parser = Parser(response.text)

        dom = parser.parse()

        rss_builder = RSSBuilder(dom, self.config.limit)

        feed = rss_builder.build_feed()

        if self.config.json:
            feed = feed.json()
            parsed_json = json.loads(feed)
            feed = json.dumps(parsed_json, indent=4)

        print(feed)
