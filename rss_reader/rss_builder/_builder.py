from rss_reader.rss_builder.rss_models import Feed
from rss_reader.rss_builder.url_resolver import URLResolver


class RSSBuilder:
    def __init__(self, dom, limit, check_urls):
        self.dom = dom
        self.limit = limit
        self.check_urls = check_urls

    @staticmethod
    def _get_element_text(element, tag_name):
        try:
            return " ".join(part for part in element.find(tag_name).find_text() if part)
        except AttributeError:
            return ""

    def build_feed(self) -> Feed:
        def limitation_gen(limit):
            """Helper generator function to yield limited amount of items."""
            i = 1
            while i != limit + 1:
                yield i
                i += 1

        all_urls = {
            i: set(item.find_urls())
            for i, item in zip(limitation_gen(self.limit), self.dom.find_all("item"))
        }

        url_qualifier = URLResolver(all_urls, self.check_urls)

        determined_urls = url_qualifier.determine_urls()

        feed_items = []

        for i, item in zip(limitation_gen(self.limit), self.dom.find_all("item")):
            feed_link = self._get_element_text(item, "link")

            images = list(
                map(
                    lambda url: url[1],
                    filter(lambda url: url[0] == i, determined_urls["image"]),
                )
            )
            audios = list(
                map(
                    lambda url: url[1],
                    filter(lambda url: url[0] == i, determined_urls["audio"]),
                )
            )
            others = list(
                map(
                    lambda url: url[1],
                    filter(
                        lambda url: url[0] == i and url[1] != feed_link,
                        determined_urls["other"],
                    ),
                )
            )

            feed_item = {
                "id": i,
                "title": self._get_element_text(item, "title"),
                "description": self._get_element_text(item, "description"),
                "link": feed_link,
                "author": self._get_element_text(item, "author"),
                "pubDate": self._get_element_text(item, "pubDate"),
                "links": {
                    "images": images,
                    "audios": audios,
                    "others": others,
                },
            }
            feed_items.append(feed_item)

        feed_data = {
            "title": self._get_element_text(self.dom, "title"),
            "description": self._get_element_text(self.dom, "description"),
            "link": self._get_element_text(self.dom, "link"),
            "image": self._get_element_text(self.dom.find("image"), "url"),
            "language": self._get_element_text(self.dom, "language"),
            "items": feed_items,
        }

        return Feed(**feed_data)
