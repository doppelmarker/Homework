from typing import Optional

from pydantic import BaseModel, root_validator


class Item(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str]
    author: Optional[str]
    pubDate: Optional[str]

    @root_validator
    def either_title_or_description(cls, values):
        title, description = values.get("title"), values.get("description")
        assert not (
            title is None and description is None
        ), f"either title or description must be present in Item"
        return values

    def __str__(self):
        fields = self.__dict__
        result = ""
        for field in fields:
            if field == "id":
                result += f"Item {fields[field]}\n  "
            elif fields[field] is not None:
                result += f"{field.capitalize()}: {fields[field]}\n  "
        return result


class Feed(BaseModel):
    title: str
    description: str
    link: str
    items: list[Item]

    def __str__(self):
        return (
            f"Feed: {self.title}\nDescription: {self.description}\nLink: "
            f"{self.link}\nItems:\n{chr(10).join((str(item) for item in self.items))} "
        )
