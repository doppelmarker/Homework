import requests

from rss_reader.config import config
from rss_reader.rss_builder import RSSBuilder
from rss_reader.xml_parser import Parser


class Reader:
    def __init__(self):
        self.link = config.source

    def start(self):
        response = requests.get(self.link)

        parser = Parser(response.text)

        dom = parser.parse()

        rss_builder = RSSBuilder(dom, config.limit)

        feed = rss_builder.build_feed()

        print(feed)
