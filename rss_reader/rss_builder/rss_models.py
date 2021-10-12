from typing import Optional

from pydantic import BaseModel, root_validator


class Item(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str]
    author: Optional[str]
    pubDate: Optional[str]
    links: Optional[dict]

    @root_validator
    def either_title_or_description(cls, values):
        title, description = values.get("title"), values.get("description")
        assert not (
            title is None and description is None
        ), f"either title or description must be present in Item"
        return values


class Feed(BaseModel):
    title: str
    description: str
    link: str
    image: Optional[str]
    language: Optional[str]
    items: Optional[list[Item]]
