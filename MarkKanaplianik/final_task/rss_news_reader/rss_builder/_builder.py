"""Module providing logics on building RSS feeds."""
from rss_news_reader.xml_parser import Element

from ._rss_models import Feed
from ._url_resolver import URLResolver


class RSSBuilder:
    """Class to build RSS feed based on dom object of parsed XML."""

    def __init__(self, dom: Element, limit: int, check_urls: bool):
        self.dom = dom
        self.limit = limit
        self.check_urls = check_urls

    def build_feed(self) -> Feed:
        """Public method to build RSS Feed. At the beginning it collects all urls from items in XML dom object to
        resolve their types, after that RSS items are built with resolved urls."""

        def limitation_gen(limit: int):
            """Helper generator function to yield limited amount of items. Used in conjunction with zip function."""
            i = 1
            while i != limit + 1:
                yield i
                i += 1

        all_urls = {
            i: set(item.find_urls())
            for i, item in zip(
                limitation_gen(self.limit), self.dom.find_all("item", nested=False)
            )
        }

        url_resolver = URLResolver(all_urls, self.check_urls)

        resolved_urls = url_resolver.resolve_urls()

        feed_items = []

        for i, item in zip(
            limitation_gen(self.limit), self.dom.find_all("item", nested=False)
        ):
            item_link = item.get_element_text("link")

            images = list(
                map(
                    lambda url: url.source,
                    filter(lambda url: url.item_num == i, resolved_urls["image"]),
                )
            )
            audios = list(
                map(
                    lambda url: url.source,
                    filter(lambda url: url.item_num == i, resolved_urls["audio"]),
                )
            )
            others = list(
                map(
                    lambda url: url.source,
                    filter(
                        lambda url: url.item_num == i and url.source != item_link,
                        resolved_urls["other"],
                    ),
                )
            )

            feed_item = {
                "id": i,
                "title": item.get_element_text("title"),
                "description": item.get_element_text("description"),
                "link": item_link,
                "author": item.get_element_text("author"),
                "pubDate": item.get_element_text("pubDate"),
                "links": {
                    "images": images,
                    "audios": audios,
                    "others": others,
                },
            }
            feed_items.append(feed_item)

        feed_data = {
            "title": self.dom.get_element_text("title"),
            "description": self.dom.get_element_text("description"),
            "link": self.dom.get_element_text("link"),
            "image": self.dom.find("image").get_element_text("url"),
            "language": self.dom.get_element_text("language"),
            "items": feed_items,
        }

        return Feed(**feed_data)
