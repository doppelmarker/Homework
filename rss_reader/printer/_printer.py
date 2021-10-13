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
                print(
                    f"Feed: {feed.title}\n\n{feed.description}\n\nLink: {feed.link}\n"
                )
                if feed.image:
                    print(f"Image: {feed.image}\n")
                for item in feed.items:
                    print(f"Item {item.id}:", end="\n\n   ")
                    if item.title:
                        print(f"Title: {item.title}", end="\n\n   ")
                    if item.description:
                        print(f"{item.description}", end="\n\n   ")
                    if item.link:
                        print(f"Link: {item.link}", end="\n\n   ")
                    if item.author:
                        print(f"Author: {item.author}", end="\n\n   ")
                    if item.pubDate:
                        print(f"Publication date: {item.pubDate}", end="\n\n   ")
                    if item.links:
                        print(f"Links:", end="\n")
                        for name, named_links in item.links.items():
                            if named_links:
                                print(f"      {name}:\n         ", end="")
                            for i, link in enumerate(named_links, start=1):
                                print(f"[{i}]: {link}\n         ", end="")
                            print()
                    print()

    def print(self, feeds: List[Feed]):
        self._print_to_console(feeds)
        if self.converter:
            self._print_converted(feeds)
