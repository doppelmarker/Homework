import json
import logging
from typing import List

from colorama import Back, Fore, Style, init
from pydantic import BaseModel

from rss_reader.rss_builder.rss_models import Feed

logger = logging.getLogger("rss-reader")


class JSONFeeds(BaseModel):
    """Model to handle a list of feeds when converting them to json format."""

    feeds: List[Feed]


class NewsPrinter:
    def __init__(self, _to_json, colorize):
        self.to_json = _to_json
        self.colorize = colorize

    @staticmethod
    def _to_json(model: BaseModel):
        model = model.json()
        parsed_json = json.loads(model)
        model = json.dumps(parsed_json, indent=4, ensure_ascii=False)
        return model

    @staticmethod
    def _print_uncolored(feeds: List[Feed]):
        for feed in feeds:
            print(f"Feed: {feed.title}\n\n{feed.description}\n\nLink: {feed.link}\n")
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

    @staticmethod
    def _print_colored(feeds: List[Feed]):
        init()
        for feed in feeds:
            print(Back.RED + "\n" + Style.RESET_ALL, end="")
            print(
                Style.NORMAL
                + Fore.LIGHTWHITE_EX
                + Back.RED
                + f"\nFeed: {feed.title}\n"
                + Style.RESET_ALL,
                end="",
            )
            print(
                Style.NORMAL
                + Fore.LIGHTWHITE_EX
                + Back.LIGHTBLUE_EX
                + f"\n{feed.description}\n"
                + Style.RESET_ALL,
                end="",
            )
            print(
                Style.NORMAL
                + Fore.LIGHTWHITE_EX
                + Back.RED
                + f"\nLink: {feed.link}\n"
                + Style.RESET_ALL,
                end="",
            )
            if feed.image:
                print(
                    Style.NORMAL
                    + Fore.LIGHTWHITE_EX
                    + Back.RED
                    + f"\nImage: {feed.image}\n"
                    + Style.RESET_ALL,
                    end="",
                )
            for i, item in enumerate(feed.items, start=1):
                if i % 2 == 1:
                    print(
                        Style.NORMAL
                        + Fore.LIGHTWHITE_EX
                        + Back.LIGHTBLACK_EX
                        + f"\nItem {item.id}:",
                        end="\n\n   ",
                    )
                else:
                    print(
                        Style.NORMAL
                        + Fore.LIGHTBLACK_EX
                        + Back.LIGHTWHITE_EX
                        + f"\nItem {item.id}:",
                        end="\n\n   ",
                    )
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
            print(Style.RESET_ALL)

    def print(self, feeds: List[Feed]):
        if self.to_json:
            print(NewsPrinter._to_json(JSONFeeds(feeds=feeds)))
        elif self.colorize:
            NewsPrinter._print_colored(feeds)
        else:
            NewsPrinter._print_uncolored(feeds)
