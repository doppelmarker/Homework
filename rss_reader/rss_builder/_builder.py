from rss_reader.rss_builder.rss_models import Feed


class RSSBuilder:
    def __init__(self, dom, limit=None):
        self.dom = dom
        self.limit = limit

    def build_feed(self) -> Feed:
        items = list(self.dom.find_all("item"))
        if self.limit:
            items = items[: self.limit]

        data = {
            "title": self.dom.find("title").next_text,
            "description": self.dom.find("description").next_text,
            "link": self.dom.find("link").next_text,
            "items": [
                {
                    "id": i,
                    "title": item.find("title").next_text,
                    "link": item.find("link").next_text,
                    "pub_date": item.find("pubDate").next_text,
                }
                for i, item in enumerate(items, start=1)
            ],
        }

        return Feed(**data)
