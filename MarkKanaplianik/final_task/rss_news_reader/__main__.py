"""
__main__.py module makes it possible to run application as module like this: python -m rss_news_reader
"""

# add rss_news_reader package path to sys.path
import sys
from pathlib import Path

rss_reader_pkg_dir_path = str(Path(__file__).parent.resolve())
sys.path.insert(1, rss_reader_pkg_dir_path)

from rss_reader import main

if __name__ == "__main__":
    main()
