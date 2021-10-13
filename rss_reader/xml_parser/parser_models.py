import re
from typing import Optional
from urllib.parse import urljoin, urlparse

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

    @staticmethod
    def _determine_link(link: str):
        image_extensions = [".png", ".jpeg", ".jpg"]
        audio_extensions = [".mp3"]
        for image_extension in image_extensions:
            if urlparse(link).path.endswith(image_extension):
                return "image"
        for audio_extension in audio_extensions:
            if urlparse(link).path.endswith(audio_extension):
                return "audio"
        return "other"

    def find_links(self):
        for child in self.children:
            if re.match(r"http", child.text):
                yield Element._determine_link(child.text), child.text
            for attr in child.attributes:
                if re.match(r"http", attr.value):
                    yield Element._determine_link(attr.value), attr.value
            yield from child.find_links()

    def find_text(self):
        for child in self.children:
            if not child.tag_name:
                yield child.text.strip()
            yield from child.find_text()

    def __str__(self):
        return f"<{self.tag_name}>"

    def __repr__(self):
        return f"<{self.tag_name}>"
