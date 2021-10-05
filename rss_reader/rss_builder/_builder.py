from rss_reader.rss_builder.rss_models import Feed, Item


class RSSBuilder:
    def __init__(self, dom, limit=-2):
        self.dom = dom
        self.limit = limit

    def build_feed(self) -> Feed:
        items = self.dom.find_all("item")

        item_fields = Item.__fields__.keys()

        rss_items = []

        def num_gen(limit):
            i = 1
            while i != limit + 1:
                yield i
                i += 1

        for i, item in zip(num_gen(self.limit), items):
            item_data = {"id": i}
            for item_field in item_fields:
                if item_field == "links":
                    links = dict()
                    for link in item.find_links():
                        links.update(link)
                    item_data[item_field] = links
                else:
                    found_item = item.find(item_field)
                    if found_item:
                        item_data[item_field] = found_item.next_text
            rss_items.append(Item(**item_data))

        feed_data = {
            "title": self.dom.find("title").next_text,
            "description": self.dom.find("description").next_text,
            "link": self.dom.find("link").next_text,
            "items": rss_items,
        }

        return Feed(**feed_data)
