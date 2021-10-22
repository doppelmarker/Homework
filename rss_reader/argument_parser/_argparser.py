"""Module which encompasses console arguments settings and parsing logics."""
import argparse


class ArgParser:
    """Class parsing console arguments."""

    def __init__(self):
        super(ArgParser, self).__init__()
        self.parser = argparse.ArgumentParser(
            prog="markedrss",
            description="Pure Python command-line RSS reader.",
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=30
            ),
        )
        self.parser.add_argument("source", nargs="?", default=None, help="RSS URL")
        self.parser.add_argument(
            "--version", help="Print version info", action="version", version="3.2.1"
        )
        self.parser.add_argument(
            "--limit",
            help="Limit news topics if this parameter provided",
            type=int,
            default=-2,
        )
        self.parser.add_argument(
            "--json", help="Print result as JSON in stdout", action="store_true"
        )
        self.parser.add_argument(
            "--verbose", help="Output verbose status messages", action="store_true"
        )
        self.parser.add_argument(
            "--date", help="Print news published on a specific date"
        )
        self.to_html_action = self.parser.add_argument(
            "--to-html",
            nargs="?",
            help="Convert news to .html format and save them by the specified folder path",
            metavar="FOLDER_PATH",
        )
        self.to_pdf_action = self.parser.add_argument(
            "--to-pdf",
            nargs="?",
            help="Convert news to .pdf format and save them by the specified folder path",
            metavar="FOLDER_PATH",
        )
        self.to_epub_action = self.parser.add_argument(
            "--to-epub",
            nargs="?",
            help="Convert news to .epub format and save them by the specified folder path",
            metavar="FOLDER_PATH",
        )
        self.parser.add_argument(
            "--colorize", help="Print news in colorized mode", action="store_true"
        )
        self.parser.add_argument(
            "--check-urls",
            help="Ensure url represents an image (requires installation of additional dependency, use: pip install "
            "markedrss[aiohttp])",
            action="store_true",
        )

    @property
    def args(self) -> argparse.Namespace:
        """Property field to return parsed console arguments."""
        return self.parser.parse_args()
