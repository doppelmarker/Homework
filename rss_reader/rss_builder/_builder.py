from collections import ChainMap

from rss_reader.rss_builder.rss_models import Feed


class RSSBuilder:
    def __init__(self, dom, limit):
        self.dom = dom
        self.limit = limit

    @staticmethod
    def _get_element_text(element, tag_name):
        try:
            return element.find(tag_name).next_text
        except AttributeError:
            return ""

    def build_feed(self) -> Feed:
        items = self.dom.find_all("item")

        def limitation_gen(limit):
            """Helper generator function to yield limited amount of items."""
            i = 1
            while i != limit + 1:
                yield i
                i += 1

        feed_data = {
            "title": self._get_element_text(self.dom, "title"),
            "description": self._get_element_text(self.dom, "description"),
            "link": self._get_element_text(self.dom, "link"),
            "image": self._get_element_text(self.dom.find("image"), "url"),
            "language": self._get_element_text(self.dom, "language"),
            "items": [
                {
                    "id": i,
                    "title": self._get_element_text(item, "title"),
                    "description": self._get_element_text(item, "description"),
                    "link": self._get_element_text(item, "link"),
                    "author": self._get_element_text(item, "author"),
                    "pubDate": self._get_element_text(item, "pubDate"),
                    "links": dict(ChainMap(*item.find_links())),
                }
                for i, item in zip(limitation_gen(self.limit), items)
            ],
        }

        return Feed(**feed_data)
