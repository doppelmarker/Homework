"""Module contains models for representing parsed XML data structures."""
import re
from typing import Optional

from pydantic import BaseModel


class Attribute(BaseModel):
    """Represents an attribute inside XML tag."""

    name: str
    value: str


class Element(BaseModel):
    """Represents an element of XML dom tree."""

    tag_name: Optional[str]
    attributes: Optional[list[Attribute]] = []
    parent: Optional["Element"]
    children: Optional["list[Element]"] = []
    text: Optional[str]

    def find_all(self, tag_name: str, *, nested: bool = True):
        """
        Generator method yielding all elements having a given tag_name in the subtree of the current element.\n
        By default, nested parameter is equal to True, this means that find_all will traverse the whole subtree of the
        given element.\n
        If nested is set to False, than it is implied that elements to be searched for don't contain
        other elements with the same tag_name.\n
        Summing up, if XML structure is rather complicated, and we are acknowledged that searched elements don't
        contain elements with the same tag_name, then providing this option may drastically speed up elements searching.
        """
        for child in self.children:
            if child.tag_name == tag_name:
                yield child
                if not nested:
                    continue
            yield from child.find_all(tag_name)

    def find(self, tag_name: str) -> "Element":
        """Returns the next element with the given tag_name in the subtree relatively to the current one."""
        for child in self.children:
            if child.tag_name == tag_name:
                return child
            else:
                next_child = child.find(tag_name)
            try:
                if next_child.tag_name == tag_name:
                    return next_child
            except AttributeError:
                pass

    def find_urls(self):
        """Generator method yielding all URLs in the subtree of the given element. Element's text for URL presence is
        explored as well as its attributes."""
        for child in self.children:
            if re.match("http", child.text):
                yield child.text
            for attr in child.attributes:
                if re.match("http", attr.value):
                    yield attr.value
            yield from child.find_urls()

    def _find_text(self):
        """Generator method yielding all stripped text occurrences in the subtree of the current element."""
        for child in self.children:
            if not child.tag_name:
                yield child.text.strip()
            yield from child._find_text()

    def get_element_text(self, tag_name: str):
        """Returns concatenated text occurrences in the subtree of the item specified by the given tag_name, which,
        in turn, is situated in the subtree of the current item."""
        try:
            return " ".join(part for part in self.find(tag_name)._find_text() if part)
        except AttributeError:
            return ""

    def __str__(self):
        return f"<{self.tag_name}>"

    def __repr__(self):
        return f"<{self.tag_name}>"
