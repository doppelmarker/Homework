import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Pure Python command-line RSS reader."
        )
        self.parser.add_argument("source", nargs="?", default=None, help="RSS URL")
        self.parser.add_argument(
            "--version", help="Print version info", action="version", version="2.9.9"
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
            help="Convert news to .html format and save them by the specified path",
            metavar="PATH",
        )
        self.parser.add_argument(
            "--to-pdf",
            type=str,
            help="Convert news to .pdf format and save them by the specified path",
            metavar="PATH",
        )

    @property
    def args(self):
        return self.parser.parse_args()
