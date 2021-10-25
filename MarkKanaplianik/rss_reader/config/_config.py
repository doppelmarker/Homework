"""
Application's configuration module. Contains path configuration logics.
Provides Config class, its instance possesses fields representing passed console arguments.
These fields are subsequently used to adjust the workflow of the application.
"""
import logging
import sys
from configparser import ConfigParser
from os import mkdir
from pathlib import Path

from MarkKanaplianik.rss_reader.argument_parser import ArgParser

config_logger = logging.getLogger("config")
# if --verbose not passed, config_logger doesn't print logs to console
config_logger.setLevel("CRITICAL")
main_logger = logging.getLogger("rss-reader")

# default application directory
default_reader_dir_path = Path(Path.home(), "rss_reader")


class Config(ArgParser, ConfigParser):
    """Class, whose instances hold fields representing passed console arguments. It configures the application."""

    def __init__(self):
        super(Config, self).__init__()
        self.source = None
        self.limit = None
        self.json = None
        self.verbose = None
        self.cached = None
        self.format = {}
        self.check_urls = None
        self.colorize = None
        self.clear_cache = None

        self.cache_file_path = None
        self._log_dir_path = None
        self._cache_dir_path = None

    def _set_defaults(self, default_reader_dir_path_: Path) -> None:
        """Sets default dir paths. If a valid DEFAULT_DIR_PATH is set in .ini file, it overrides the original one."""
        global default_reader_dir_path
        default_reader_dir_path = default_reader_dir_path_
        self._log_dir_path = default_reader_dir_path_
        self._cache_dir_path = default_reader_dir_path_
        self.to_html_action.const = default_reader_dir_path_
        self.to_pdf_action.const = default_reader_dir_path_
        self.to_epub_action.const = default_reader_dir_path_

    def _load_ini(self) -> None:
        """Loads config from .ini file, which should be located in rss_reader package on the same level with
        __main__.py ."""
        self.read(Path(sys.path[0], "rss_reader.ini"))
        if "rss-reader" not in self.sections() or not self["rss-reader"]:
            config_logger.info(
                ".ini file is not configured. Running with default settings..."
            )
            return

        if default_dir_path := self["rss-reader"].get("DEFAULT_DIR_PATH", None):
            if Config._is_ini_default_dir_path_valid(Path(default_dir_path)):
                self._set_defaults(Path(default_dir_path))
        if cache_dir_path := self["rss-reader"].get("CACHE_DIR_PATH", None):
            self._cache_dir_path = Path(cache_dir_path)
        if log_dir_path := self["rss-reader"].get("LOG_DIR_PATH", None):
            self._log_dir_path = Path(log_dir_path)
        if convert_dir_path := self["rss-reader"].get("CONVERT_DIR_PATH", None):
            self.to_html_action.const = Path(convert_dir_path)
            self.to_pdf_action.const = Path(convert_dir_path)
            self.to_epub_action.const = Path(convert_dir_path)

    def _set_verbose(self) -> None:
        """Sets verbose mode if --verbose argument was passed."""
        self.verbose = self.args.verbose

    def _load_cli(self) -> None:
        """Loads command line arguments to config."""
        cli_args = self.args
        self.source = cli_args.source
        self.limit = cli_args.limit
        self.json = cli_args.json
        self.cached = cli_args.date
        if cli_args.to_html:
            self.format.update(html=cli_args.to_html)
        if cli_args.to_pdf:
            self.format.update(pdf=cli_args.to_pdf)
        if cli_args.to_epub:
            self.format.update(epub=cli_args.to_epub)
        self.colorize = cli_args.colorize
        self.check_urls = cli_args.check_urls
        self.clear_cache = cli_args.clear_cache

    @staticmethod
    def _is_ini_default_dir_path_valid(dir_path: Path) -> bool:
        """Checks whether default dir path in .ini config is valid."""
        try:
            if not Path(dir_path).is_dir():
                mkdir(dir_path)
            return True
        except OSError:
            config_logger.warning(
                f"DEFAULT_DIR_PATH={dir_path} in .ini file is invalid! Default dir path is preserved."
            )
            return False

    @staticmethod
    def _make_file(dir_path: Path, file_name: str) -> None:
        """
        Generic method to build directory and file with the given dir_path and file_name. If file already exists,
        then nothing is done. The purpose of this method is to handle possible exceptions connected with invalid
        paths specified either as cli arguments or inside .ini file.

        Raises
        ------
        PermissionError
            if the user has not enough rights to create dir/file with the specified path

        NotADirectoryError
            if the specified dir_path is invalid
        """
        if not Path(dir_path).is_dir():
            mkdir(dir_path)
        file_path = Path(dir_path, file_name)
        Path(file_path).touch()

    def _make_logs(self) -> None:
        """
        Makes logs directory both with rss_reader.log file. If the specified LOG_DIR_PATH in the .ini file was absent or
        invalid, then logs' directory becomes DEFAULT_DIR_PATH from .ini file. But if then DEFAULT_DIR_PATH is either
        absent or invalid in .ini file, then logs' directory becomes the default application directory.
        """
        try:
            Config._make_file(self._log_dir_path, "rss_reader.log")
        except OSError:
            config_logger.warning(
                f"'{self._log_dir_path}' is not a valid dir path for storing log file. Log file will be stored "
                f"in '{default_reader_dir_path}'. "
            )
            Config._make_file(default_reader_dir_path, "rss_reader.log")

    def _make_cache(self) -> None:
        """
        Makes cache directory both with cache.json file. If the specified CACHE_DIR_PATH in the .ini file was absent or
        invalid, then cache's directory becomes DEFAULT_DIR_PATH from .ini file. But if then DEFAULT_DIR_PATH is either
        absent or invalid in .ini file, then cache's directory becomes the default application directory.
        """
        try:
            Config._make_file(self._cache_dir_path, "cache.json")
            self.cache_file_path = Path(self._cache_dir_path, "cache.json")
        except OSError:
            config_logger.warning(
                f"'{self._cache_dir_path}' is not a valid dir path for storing cache file. Cache file will be "
                f"stored in '{default_reader_dir_path}'."
            )
            Config._make_file(default_reader_dir_path, "cache.json")
            self.cache_file_path = Path(default_reader_dir_path, "cache.json")

        if self.clear_cache:
            open(self.cache_file_path, "w").close()
            config_logger.info(
                f"Cache file in {self.cache_file_path} has been successfully cleared!"
            )

    def _make_convert_files(self) -> None:
        r"""
        Makes a directory for converted files specified in command line (e.g. --to-html, --to-pdf) and these files.

        Command line arguments have the highest priority of choosing the converted files' folder
        (e.g. if --to-html C:\\rss_reader2.0 is specified in cli, then it will be superior to
        any other configurations made in .ini file).

        After that, the converted files' directory resolution
        order is the following, from highest to lowest priority: CONVERT_DIR_PATH->DEFAULT_DIR_PATH->default
        application directory.
        """
        for f in self.format:
            try:
                Config._make_file(self.format[f], f"news.{f}")
            except OSError:
                config_logger.warning(
                    f"'{f}' is not a valid dir path for storing converted files. Converted "
                    f"files will be stored in '{default_reader_dir_path}'."
                )
                Config._make_file(default_reader_dir_path, f"news.{f}")

    def _make_files(self) -> None:
        """Makes all the necessary files for the application to work."""
        self._make_logs()
        self._make_cache()
        self._make_convert_files()

    def setup(self) -> None:
        """
        Public method of Config class, which does the whole configuration job:

        - sets up the 'config' logger and the application 'rss-reader' logger;

        - loads .ini file config;

        - loads cli arguments;

        - makes all the necessary files;

        - provides logics of initial user notification about possible activation of verbose and advanced url
        resolving modes depending on incoming console arguments;

        - validates whether either source url or date arguments were passed by user.
        """
        self._set_verbose()

        # if --verbose passed, config logs are printed to console
        if self.verbose:
            config_logger.setLevel("INFO")

        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s [%(name)s] (%(module)s.py:%(funcName)s) = %(message)s"
        )
        s_handler = logging.StreamHandler()
        s_handler.setFormatter(formatter)

        config_logger.addHandler(s_handler)

        # setting default paths
        self._set_defaults(default_reader_dir_path)
        # loading .ini file
        self._load_ini()
        # loading cli arguments after setting default values for --to-html, --to-pdf, --to-epub when
        # they are not given paths in console
        self._load_cli()
        # trying to create necessary dirs and files after setting paths passed from .ini config;
        # if it's not possible for some reason, then warning about file storage redirection is shown
        self._make_files()

        if not self.source and not self.cached:
            # passing --clear-cache without source or --date is considered to be a normal behaviour
            if self.clear_cache:
                print(
                    "Program finished after clearing cache because neither [source], nor [--date DATE] args "
                    "were passed."
                )
                if not self.verbose:
                    print("For more details consider using --verbose")
                self.parser.exit()

            self.parser.error("Neither [source], nor [--date DATE] args were passed!")

        f_handler = logging.FileHandler(
            Path(self._log_dir_path, "rss_reader.log"), mode="a"
        )
        f_handler.setFormatter(formatter)
        # main logger's logs higher than 'WARNING' are always printed to .log file
        f_handler.setLevel("INFO")

        main_logger.addHandler(s_handler)
        main_logger.addHandler(f_handler)

        if self.verbose:
            main_logger.setLevel("INFO")
            main_logger.info("Enabled verbose mode.")
        else:
            main_logger.addHandler(logging.NullHandler())
            main_logger.propagate = False

        if self.check_urls and not self.cached:
            main_logger.info("Enabled advanced URL resolving mode.")
