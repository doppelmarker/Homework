from typing import List

from rss_reader.convert import to_json
from rss_reader.rss_builder.rss_models import Feed


class NewsPrinter:
    def __init__(self, converter, _to_json=False):
        self.converter = converter
        self.to_json = _to_json

    def _print_converted(self, feeds: List[Feed]):
        self.converter.convert(feeds)

    def _print_to_console(self, feeds: List[Feed]):
        if self.to_json:
            for feed in feeds:
                print(to_json(feed))
        else:
            for feed in feeds:
                print(f"Feed: {feed.title}\n{feed.description}\nLink: {feed.link}")
                if feed.image:
                    print(f"Image: {feed.image}\n")
                for item in feed.items:
                    print(f"Item {item.id}:\n   ", end="")
                    if item.title:
                        print(f"Title: {item.title}\n   ", end="")
                    if item.description:
                        print(f"{item.description}\n   ", end="")
                    if item.link:
                        print(f"Link: {item.link}\n   ", end="")
                    if item.author:
                        print(f"Author: {item.author}\n   ", end="")
                    if item.pubDate:
                        print(f"Publication date: {item.pubDate}\n   ", end="")
                    if item.links:
                        print(f"All links:\n      ", end="")
                        for i, link in enumerate(item.links.items(), start=1):
                            print(f"[{i}]: {link[1]} ({link[0]})\n      ", end="")
                    print()

    def print(self, feeds: List[Feed]):
        self._print_to_console(feeds)
        if self.converter:
            self._print_converted(feeds)
