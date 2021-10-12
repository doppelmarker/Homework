import json
from pathlib import Path
from typing import List

from jinja2 import Template
from pydantic import BaseModel

from rss_reader.rss_builder.rss_models import Feed


def to_json(model: BaseModel):
    model = model.json()
    parsed_json = json.loads(model)
    model = json.dumps(parsed_json, indent=4, ensure_ascii=False)
    return model


class Converter:
    def __init__(self, fmt):
        self.fmt = fmt
        self.module_dir = Path(__file__).parent

    def _get_html(self, **kwargs):
        template = Template(
            open(Path(self.module_dir, "feed_html_template.jinja2")).read()
        )
        return template.render(**kwargs)

    def _to_html(self, feeds: List[Feed]):
        file_path = Path(self.fmt["html"], "news.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self._get_html(feeds=feeds))

        # logger.info(f"Saved html in {file_path}")

    def _to_pdf(self, feeds: List[Feed]):
        raise NotImplementedError

    def convert(self, feeds: List[Feed]):
        if "html" in self.fmt:
            self._to_html(feeds)
        if "pdf" in self.fmt:
            self._to_pdf(feeds)
