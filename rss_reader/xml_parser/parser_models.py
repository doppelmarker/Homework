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

    def find_urls(self):
        for child in self.children:
            if re.match("http", child.text):
                yield child.text
            for attr in child.attributes:
                if re.match("http", attr.value):
                    yield attr.value
            yield from child.find_urls()

    def find_text(self):
        for child in self.children:
            if not child.tag_name:
                yield child.text.strip()
            yield from child.find_text()

    def __str__(self):
        return f"<{self.tag_name}>"

    def __repr__(self):
        return f"<{self.tag_name}>"
