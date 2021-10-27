"""Module keeps the logic of printing parsed feeds."""
import json
from typing import List

from colorama import Back, Fore, Style, init
from pydantic import BaseModel

from rss_news_reader.rss_builder import Feed, Item


class JSONFeeds(BaseModel):
    """Model to handle a list of feeds when converting them to json format."""

    feeds: List[Feed]


class NewsPrinter:
    """Class for printing parsed feeds to console. Depending on whether --colorize argument was passed,
    news are printed either colored or not."""

    def __init__(self, to_json: bool, colorize: bool):
        self.to_json = to_json
        self.colorize = colorize

    @staticmethod
    def _to_json(model: BaseModel):
        """Method to convert feeds to json format."""
        model = model.json()
        parsed_json = json.loads(model)
        model = json.dumps(parsed_json, indent=4, ensure_ascii=False)
        return model

    @staticmethod
    def _print_item_stuffing(item: Item):
        """Print the major part of an Item."""
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
        if any(item.links.values()):
            print(f"Links:", end="\n")
            for name, named_links in item.links.items():
                if named_links:
                    print(f"      {name}:\n         ", end="")
                    for i, link in enumerate(named_links, start=1):
                        print(f"[{i}]: {link}\n         ", end="")
                    print()

    @staticmethod
    def _print_uncolored(feeds: List[Feed]):
        """Prints news without colorizing."""
        for feed in feeds:
            print(f"Feed: {feed.title}\n\n{feed.description}\n\nLink: {feed.link}\n")
            if feed.image:
                print(f"Image: {feed.image}\n")
            for i, item in enumerate(feed.items, start=1):
                print(f"Item {i}:", end="\n\n   ")
                NewsPrinter._print_item_stuffing(item)
                print()

    @staticmethod
    def _print_colored(feeds: List[Feed]):
        """
        Prints colorized news.
        Attention! Colorization strongly depends on the type of the terminal the final user
        utilizes and may look rather clumsy in some of them.
        """
        # colorama's init
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
                        + f"\nItem {i}:",
                        end="\n\n   ",
                    )
                else:
                    print(
                        Style.NORMAL
                        + Fore.LIGHTBLACK_EX
                        + Back.LIGHTWHITE_EX
                        + f"\nItem {i}:",
                        end="\n\n   ",
                    )
                NewsPrinter._print_item_stuffing(item)
            print(Style.RESET_ALL)

    def print(self, feeds: List[Feed]):
        """Public method to print obtained feeds to console."""
        if self.to_json:
            print(NewsPrinter._to_json(JSONFeeds(feeds=feeds)))
        elif self.colorize:
            NewsPrinter._print_colored(feeds)
        else:
            NewsPrinter._print_uncolored(feeds)
