r"""
Module which includes logics on feeds' conversion to supported formats. Currently supported formats for
conversion: .html, .pdf, .epub. By default, converted files are stored in ..\Users\Username\rss_reader. However,
this can be changed by passing another directory path to appropriate console arguments --to-html, --to-pdf and
--to--epub. Converted file name will be 'news' followed by file extension.
"""

import logging
import os
import warnings
from pathlib import Path
from typing import List

from ebooklib import epub
from jinja2 import Template
from xhtml2pdf import pisa

from rss_reader.rss_builder.rss_models import Feed

logger = logging.getLogger("rss-reader")


class Converter:
    """Class providing public convert method, which converts collected feeds to either of supported formats specified
    by the provided console arguments: --to-html, --to-pdf, --to-epub."""

    def __init__(self, fmt: dict[str, str]):
        self.fmt = fmt
        self.module_dir = Path(__file__).parent

    def _get_html(self, **kwargs) -> str:
        """Provides a rendered html-template, which is represented as a string, for future usage in conversion to
        .html or .pdf formats."""
        template = Template(open(Path(self.module_dir, "html_template.jinja2")).read())
        return template.render(**kwargs)

    def _get_xhtml(self, **kwargs) -> str:
        """Provides a rendered xhtml-template, which is represented as a string, for future usage in conversion to
        .epub format."""
        template = Template(open(Path(self.module_dir, "xhtml_template.jinja2")).read())
        return template.render(**kwargs)

    def _to_html(self, feeds: List[Feed]) -> None:
        """Provides functionality to convert feeds to .html format."""
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
            logger.info(f"Saved html in {file_path}.")

    def _to_pdf(self, feeds: List[Feed]) -> None:
        """Provides functionality to convert feeds to .pdf format."""
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
                    logger.warning("Some error occurred when converting feeds to pdf!")

        except FileNotFoundError:
            logger.warning(
                f"Failed to save pdf file. Seems directory {dir_path} doesn't exist."
            )
        except Exception:
            logger.warning(f"Failed to save pdf file. Check your internet connection.")
            os.remove(file_path)
        else:
            logger.info(f"Saved pdf in {file_path}.")

    def _to_epub(self, feeds: List[Feed]) -> None:
        """Provides functionality to convert feeds to .epub format."""
        dir_path = self.fmt["epub"]
        file_path = Path(dir_path, "news.epub")

        book = epub.EpubBook()
        book.set_identifier("id")
        book.set_title("RSS News")
        book.set_language("en")

        toc = []
        spine = ["nav"]

        for feed in feeds:
            for num, item in enumerate(feed.items, start=1):
                chapter = epub.EpubHtml(title=item.title, file_name=f"{num}.xhtml")
                chapter.content = self._get_xhtml(item=item, language=feed.language)

                book.add_item(chapter)
                spine.append(chapter)
                toc.append(epub.Section(item.title))
                toc.append(chapter)

        book.toc = tuple(toc)
        book.spine = spine

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        epub.write_epub(file_path, book)

        logger.info(f"Saved epub in {file_path}.")

    def convert(self, feeds: List[Feed]) -> None:
        """Public method to convert accumulated feeds to supported formats depending on passed console arguments."""
        if "html" in self.fmt:
            self._to_html(feeds)
        if "pdf" in self.fmt:
            self._to_pdf(feeds)
        if "epub" in self.fmt:
            self._to_epub(feeds)
