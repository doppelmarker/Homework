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

    def __str__(self):
        fields = self.__dict__
        result = ""
        for field in fields:
            if field == "id":
                result += f"Item {fields[field]}:\n   "
            elif field == "links":
                result += "\n   Links:\n   "
                for i, item in enumerate(fields[field].items(), start=1):
                    result += f"[{i}]: {item[1]} ({item[0]})\n   "
            elif fields[field] is not None:
                result += f"{field.capitalize()}: {fields[field]}\n   "
        return result


class Feed(BaseModel):
    title: str
    description: str
    link: str
    image: Optional[str]
    language: Optional[str]
    items: Optional[list[Item]]

    def __str__(self):
        return (
            f"Feed: {self.title}\nDescription: {self.description}\nLink: "
            f"{self.link}\n\n{chr(10).join((str(item) for item in self.items))} "
        )
