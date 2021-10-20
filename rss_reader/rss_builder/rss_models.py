"""Module contains models for representing prepared RSS data structures."""
from typing import Optional

from pydantic import BaseModel, root_validator


class Item(BaseModel):
    """Represents an item in final RSS Feed, it corresponds to <item> from XML document."""

    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str]
    author: Optional[str]
    pubDate: Optional[str]
    links: Optional[dict]

    @root_validator
    def either_title_or_description(cls, values):
        """Validates presence of either title or description in Item as either of them is required."""
        title, description = values.get("title"), values.get("description")
        assert not (
            title is None and description is None
        ), f"Either title or description must be present in Item!"
        return values


class Feed(BaseModel):
    """Represents the prepared RSS Feed data structure."""

    title: str
    description: str
    link: str
    image: Optional[str]
    language: Optional[str]
    items: Optional[list[Item]]
