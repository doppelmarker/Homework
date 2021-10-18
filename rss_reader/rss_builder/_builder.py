from rss_reader.rss_builder.rss_models import Feed
from rss_reader.rss_builder.url_resolver import URLResolver


class RSSBuilder:
    def __init__(self, dom, limit, check_urls):
        self.dom = dom
        self.limit = limit
        self.check_urls = check_urls

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

        url_resolver = URLResolver(all_urls, self.check_urls)

        determined_urls = url_resolver.determine_urls()

        feed_items = []

        for i, item in zip(limitation_gen(self.limit), self.dom.find_all("item")):
            feed_link = item.get_element_text("link")

            images = list(
                map(
                    lambda url: url.source,
                    filter(lambda url: url.item_num == i, determined_urls["image"]),
                )
            )
            audios = list(
                map(
                    lambda url: url.source,
                    filter(lambda url: url.item_num == i, determined_urls["audio"]),
                )
            )
            others = list(
                map(
                    lambda url: url.source,
                    filter(
                        lambda url: url.item_num == i and url.source != feed_link,
                        determined_urls["other"],
                    ),
                )
            )

            feed_item = {
                "id": i,
                "title": item.get_element_text("title"),
                "description": item.get_element_text("description"),
                "link": feed_link,
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
