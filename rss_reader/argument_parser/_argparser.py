import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Pure Python command-line RSS reader."
        )
        self.parser.add_argument("source", nargs="?", default=None, help="RSS URL")
        self.parser.add_argument(
            "--version", help="Print version info", action="version", version="2.0.0"
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

    @property
    def args(self):
        return self.parser.parse_args()
