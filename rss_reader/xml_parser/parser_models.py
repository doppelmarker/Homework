import re
from typing import Optional

from pydantic import BaseModel


class Attribute(BaseModel):
    name: str
    value: str


class Element(BaseModel):
    tag_name: Optional[str]
    attributes: Optional[list[Attribute]] = []
    parent: Optional["Element"]
    children: Optional["list[Element]"] = []
    text: Optional[str]

    def find_all(self, tag_name):
        for child in self.children:
            if child.tag_name == tag_name:
                yield child
                continue
            yield from child.find_all(tag_name)

    def find(self, tag_name):
        for child in self.children:
            if child.tag_name != tag_name:
                a = child.find(tag_name)
            else:
                return child
            try:
                if a.tag_name == tag_name:
                    return a
            except AttributeError:
                pass

    def find_links(self):
        for child in self.children:
            if re.match(r"http", child.text):
                yield {"link" if child.tag_name is None else child.tag_name: child.text}
            for attr in child.attributes:
                if re.match(r"http", attr.value):
                    yield {child.tag_name: attr.value}
            yield from child.find_links()

    @property
    def next_text(self):
        return self.find(None).text

    def __str__(self):
        return f"<{self.tag_name}>"
