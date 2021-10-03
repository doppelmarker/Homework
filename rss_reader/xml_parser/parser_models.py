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

    @property
    def next_text(self):
        return self.find(None).text

    def __str__(self):
        return f"<{self.tag_name}>"
