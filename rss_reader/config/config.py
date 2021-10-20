"""
Application's configuration module. Contains path configuration logics.
Provides instance of Config class, this instance possesses fields representing passed console arguments.
These fields are subsequently used to adjust the workflow of the application.
"""
import argparse
import logging
from os import mkdir
from pathlib import Path

from rss_reader.argument_parser import ArgParser

logger = logging.getLogger("rss-reader")


class Config:
    """
    Class, whose instances hold fields representing passed console arguments, path of the utility directory,
    where cache file will be precisely stored. Also, by default, all feeds converted to supported formats are stored
    by the exact same path, if corresponding arguments such like --to-html where not passed with other directory
    path to redetermine where to save these files to.
    """

    def __init__(self, reader_dir_path: Path, cache_file_path: Path):
        self.reader_dir_path = reader_dir_path
        self.cache_file_path = cache_file_path
        self.source = None
        self.limit = None
        self.json = None
        self.verbose = None
        self.cached = None
        self.format = {}
        self.check_urls = None
        self.colorize = None

    def load_cli(self, args: argparse.Namespace) -> None:
        """Loads command line arguments to config."""
        self.source = args.source
        self.limit = args.limit
        self.json = args.json
        self.verbose = args.verbose
        self.cached = args.date
        if args.to_html:
            self.format.update(html=args.to_html)
        if args.to_pdf:
            self.format.update(pdf=args.to_pdf)
        if args.to_epub:
            self.format.update(epub=args.to_epub)
        self.colorize = args.colorize
        self.check_urls = args.check_urls

    def setup(self, arg_parser: ArgParser) -> None:
        """
        Provides logics of initial user notification about possible activation of verbose and advanced url resolving
        modes depending on incoming console arguments. Also validates whether either source url or date arguments
        were passed by user.
        """
        if self.verbose:
            formatter = logging.Formatter(
                "[%(levelname)s] %(asctime)s (%(funcName)s) = %(message)s"
            )
            logger.setLevel("DEBUG")
            s_handler = logging.StreamHandler()
            s_handler.setFormatter(formatter)
            logger.addHandler(s_handler)
            logger.info("Enabled verbose mode.")
        else:
            logger.addHandler(logging.NullHandler())
            logger.propagate = False
        if not self.source and not self.cached:
            arg_parser.parser.error(
                "Neither [source], nor [--date DATE] args were passed!"
            )
        if self.check_urls and not self.cached:
            logger.info("Enabled advanced url resolving mode.")


_arg_parser = ArgParser()

_reader_dir_path = Path(Path.home(), "rss_reader")

if not _reader_dir_path.is_dir():
    mkdir(_reader_dir_path)

# setting up default save path for supported types of feeds' conversion
_arg_parser.to_html_action.const = _reader_dir_path
_arg_parser.to_pdf_action.const = _reader_dir_path
_arg_parser.to_epub_action.const = _reader_dir_path

_cache_file_path = Path(_reader_dir_path, "cache.json")

if not _cache_file_path.is_file():
    Path(_cache_file_path).touch()

config = Config(_reader_dir_path, _cache_file_path)
config.load_cli(_arg_parser.args)
config.setup(_arg_parser)
