import json
import logging
import warnings
from pathlib import Path
from typing import List

from jinja2 import Template
from pydantic import BaseModel
from xhtml2pdf import pisa

from rss_reader.rss_builder.rss_models import Feed

logger = logging.getLogger("rss-reader")


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
        dir_path = self.fmt["html"]
        file_path = Path(dir_path, "news.html")

        try:
            with open(file_path, "w", encoding="utf-8") as result_file:
                result_file.write(self._get_html(feeds=feeds))
        except FileNotFoundError:
            logger.warning(
                f"Failed to save html file. Seems directory {dir_path} doesn't exist."
            )
        else:
            logger.info(f"Saved html in {file_path}")

    def _to_pdf(self, feeds):
        dir_path = self.fmt["pdf"]
        file_path = Path(dir_path, "news.pdf")

        try:
            with open(file_path, "w+b") as result_file, warnings.catch_warnings():
                warnings.simplefilter("ignore")

                logger.info("Converting feeds to pdf...")

                pisa_status = pisa.CreatePDF(
                    self._get_html(feeds=feeds), dest=result_file
                )

                if pisa_status.err:
                    logger.warning("Some error occurred when converting feeds to pdf")

        except FileNotFoundError:
            logger.warning(
                f"Failed to save pdf file. Seems directory {dir_path} doesn't exist."
            )
        else:
            logger.info(f"Saved pdf in {file_path}")

    def convert(self, feeds: List[Feed]):
        if "html" in self.fmt:
            self._to_html(feeds)
        if "pdf" in self.fmt:
            self._to_pdf(feeds)
