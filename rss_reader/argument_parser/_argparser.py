import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="markedrss",
            description="Pure Python command-line RSS reader.",
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=30
            ),
        )
        self.parser.add_argument("source", nargs="?", default=None, help="RSS URL")
        self.parser.add_argument(
            "--version", help="Print version info", action="version", version="3.0.0"
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
            "--date", help="Print news published on a specific date", type=str
        )
        self.parser.add_argument(
            "--to-html",
            type=str,
            help="Convert news to .html format and save them by the specified folder path",
            metavar="FOLDER_PATH",
        )
        self.parser.add_argument(
            "--to-pdf",
            type=str,
            help="Convert news to .pdf format and save them by the specified folder path",
            metavar="FOLDER_PATH",
        )
        self.parser.add_argument(
            "--check-urls",
            help="Ensure a url represents an image by sending HEAD HTTP request "
            "(requires aiohttp installation through pip install markedrss[aiohttp])",
            action="store_true",
        )

    @property
    def args(self):
        return self.parser.parse_args()
