import json
import logging
from typing import List

from pydantic import BaseModel

from rss_reader.rss_builder.rss_models import Feed

logger = logging.getLogger("rss-reader")


class NewsPrinter:
    def __init__(self, _to_json):
        self.to_json = _to_json

    @staticmethod
    def _to_json(model: BaseModel):
        model = model.json()
        parsed_json = json.loads(model)
        model = json.dumps(parsed_json, indent=4, ensure_ascii=False)
        return model

    def _print_to_console(self, feeds: List[Feed]):
        if self.to_json:
            for feed in feeds:
                print(NewsPrinter._to_json(feed))
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
