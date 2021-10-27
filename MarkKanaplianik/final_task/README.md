[![PyPI version](https://badge.fury.io/py/rss-news-reader.svg)](https://badge.fury.io/py/rss-news-reader)

# Python RSS reader

Final task for EPAM Python Training 2021.09

`rss-news-reader` is a command line utility that makes it easy to view RSS feeds in a readable format.

***Python 3.9 required***

***Tested on Windows and MacOS***

## Installation and usage

You can install it by running the following command:

    pip install rss-news-reader

Now, you can run the utility in two ways:

    rss-news-reader {YOUR ARGUMENTS}
    rss-reader {YOUR ARGUMENTS} 

*OR*

1. Clone github repository:

       git clone https://github.com/doppelmarker/Homework

2. Change directory to `/Homework/MarkKanaplianik/final_task`.

       cd .../Homework/MarkKanaplianik/final_task

3. Install necessary dependencies:

       pip install -r requirements.txt

Now, provided, your current directory is `/Homework/MarkKanaplianik/final_task`, you can run `rss_news_reader` as a
package:

    python rss_news_reader
    python -m rss_news_reader

or, provided, your current directory is `/Homework/MarkKanaplianik/final_task/rss_news_reader`, you can directly run the
module:

    python rss_reader.py

To see help message, please, use `-h/--help` argument: `rss-news-reader -h`.

    usage: rss-news-reader [-h] [-v] [--verbose] [-c] [--clear-cache] [-l LIMIT] [--json] [-d DATE] [--to-html [FOLDER_PATH]] [--to-pdf [FOLDER_PATH]] [--to-epub [FOLDER_PATH]] [--check-urls]
                 [source]

    Pure Python command-line RSS reader.

    positional arguments:
    source                   RSS URL

    optional arguments:
    -h, --help               Show this help message and exit.
    -v, --version            Print version info.
    --verbose                Output verbose status messages.
    -c, --colorize           Print news in colorized mode.
    --clear-cache            Clear cache file on startup.
    -l LIMIT, --limit LIMIT  Limit news topics if this parameter provided.
    --json                   Print result as JSON.
    -d DATE, --date DATE     Print cached news published on a specific date.
    --to-html [FOLDER_PATH]  Convert news to .html format and save it by the specified folder path (FOLDER_PATH can be omitted).
    --to-pdf [FOLDER_PATH]   Convert news to .pdf format and save it by the specified folder path (FOLDER_PATH can be omitted).
    --to-epub [FOLDER_PATH]  Convert news to .epub format and save it by the specified folder path (FOLDER_PATH can be omitted).
    --check-urls             Ensure URL represents an image (requires installation of additional dependency, use: pip install aiohttp).

*Some notes*:

+ ***IMPORTANT***: `rss-news-reader` utility name was chosen, because `rss-reader` was already taken
  on https://pypi.org/. However, it is still possible to utilize the application using `rss-reader` word:

      rss-reader {YOUR ARGUMENTS}    

+ when `--clear-cache` is passed individually, cache gets cleared and application terminates;
+ `--check-urls` requires internet connection; without passing this argument some URLs representing images may be
  ascribed to `others` category of resulting converted files.

### Additional dependencies

In order to install additional dependency to make `--check-urls` work, please, use the following command:

    pip install aiohttp

## Logging

There are 2 loggers:

+ general `rss-news-reader` application logger;
+ `config` logger.

Messages with either `WARNING` or `ERROR` severities are ***always*** printed to `rss_news_reader.log` file.

`config` logs are only printed to console.

If `--verbose` argument is ***NOT*** passed, then only messages with either `WARNING` or `ERROR` severities
of `rss_news_reader` are printed to console, `config` logs are not printed to console.

If `--verbose` argument is passed, then all `rss_news_reader` logs are printed both to console and log file,
while `config`
logs are printed to console.

## Configuration

Application creates several files:

+ `cache.json`;
+ `rss_news_reader.log`;
+ converted to supported formats files: `news.html`/`pdf`/`epub`

By default, the application files are stored inside home directory in a freshly created `rss_news_reader` folder:

    - Windows: C:\Users\User\rss_news_reader
        or C:\Users\rss_news_reader
    - Linux and MacOS: /home/rss_news_reader

You can change this by adding `rss_news_reader.ini` file either inside `rss_news_reader` **package** locally, or inside
home directory.

If `rss_news_reader.ini` files are present both inside **package** and home directory, then one inside **package**
overrides one from home directory.

The structure of `rss_news_reader.ini` file is the following:

    [rss-reader]
    DEFAULT_DIR_PATH =
    LOG_DIR_PATH =
    CACHE_DIR_PATH =
    CONVERT_DIR_PATH =

The directory path resolution order for storing files, *from lowest to highest priority*, can be found below.

For `rss_news_reader.log` file:

    home directory -> DEFAULT_DIR_PATH -> LOG_DIR_PATH 

For `cache.json` file:

    home directory -> DEFAULT_DIR_PATH -> CACHE_DIR_PATH 

For converted to supported formats files like news.`html`/`pdf`/`epub`:

    home directory -> DEFAULT_DIR_PATH -> CONVERT_DIR_PATH -> command line arguments 

If `rss_news_reader.ini` file was given an invalid path or the path was empty, then the directory path gets resolved in
the reversed order.

## Cache JSON structure

Cache represents a dictionary of URLs with according lists of dictionaries of items, preceded by a dictionary of feed
info.

*Example:*

    {
        "https://news.yahoo.com/rss/": [
            {
                "title": "Yahoo News - Latest News & Headlines",
                "description": "The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.",
                "link": "https://www.yahoo.com/news",
                "image": "http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png",
                "language": "en-US"
            },
            {
                "id": 1,
                "title": "Colombia's most wanted drug lord captured in jungle raid",
                "description": "",
                "link": "https://news.yahoo.com/colombia-announces-capture-one-most-233233294.html",
                "author": "",
                "pubDate": "2021-10-23T23:32:33Z",
                "links": {
                    "images": [],
                    "audios": [],
                    "others": [
                        "https://s.yimg.com/uu/api/res/1.2/sbSt9k2i59Ne3T5Dahi7dg--~B/aD0xNTAwO3c9MjAwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/1fc569ce977352662b4cf3039acae975",
                        "http://www.ap.org"
                    ]
                }
            },
            {
                "id": 2,
                "title": "I took a 30-hour train from New York to Miami, and the motion sickness and terrible sleep were too much for me",
                "description": "",
                "link": "https://news.yahoo.com/took-30-hour-train-york-102700276.html",
                "author": "",
                "pubDate": "2021-10-24T10:27:00Z",
                "links": {
                    "images": [],
                    "audios": [],
                    "others": [
                        "https://s.yimg.com/uu/api/res/1.2/OEoRF0WWW8IeP0etSC7D2w--~B/aD0yMjQ5O3c9MzAwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/insider_articles_922/86c1372fd1bf9d0690cac85bdcdecf5f",
                        "https://www.insider.com"
                    ]
                }
            },
            ...
        ...

*Some notes*:

+ cache auto-update mechanisms are not implemented, thus it endlessly grows; in order to clear cache
  file `--clear-cache` argument is provided;
+ `--json`-printed results are different from ones, stored in cache; user is usually not encouraged to explore and
  modify cache file (though, he is not forbidden to do so), because it's not a part of the public interface, that's why
  developers have a right to implement it in a handy manner for them, but not in a user-friendly manner,
  whereas `--json`
  argument is a part of the user interface, that's why its output is user-friendly.

`--json` output example:

     {
      "feeds": [
          {
              "title": "Yahoo News - Latest News & Headlines",
              "description": "The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.",
              "link": "https://www.yahoo.com/news",
              "image": "http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png",
              "language": "en-US",
              "items": [
                  {
                      "id": 1,
                      "title": "Colombia's most wanted drug lord captured in jungle raid",
                      "description": "",
                      "link": "https://news.yahoo.com/colombia-announces-capture-one-most-233233294.html",
                      "author": "",
                      "pubDate": "2021-10-23T23:32:33Z",
                      "links": {
                          "images": [],
                          "audios": [],
                          "others": [
                              "https://s.yimg.com/uu/api/res/1.2/sbSt9k2i59Ne3T5Dahi7dg--~B/aD0xNTAwO3c9MjAwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/1fc569ce977352662b4cf3039acae975",
                              "http://www.ap.org"
                          ]
                      }
                  },
                  ...
          ...

Why is there a list of feeds inside `--json` structure, not just a single feed? Inside cache file there may be items
with the same `pubDate`, but they may belong to different feeds. So, when there are such items and a user
passes `--date DATE` argument which represents this exact date, then these several items are returned and attributed to
several newly created `Feed` instances. After that, these `Feed` instances are printed. Printing returned news could be
implemented without respect to the feeds they belong to, but in this case it would be hard to distinguish them.

## Parsing XML

XML is parsed by parser implemented from scratch, it exploits the idea of XML *tokenization*, dom-tree is created from
tokens.

*Features*:

+ `XML CDATA` parsing support: whenever CDATA is encountered in XML, it gets recursively parsed and substituted by a
  normal text in the final form.
  \
  XML CDATA example link: https://rss.art19.com/apology-line
+ detecting `invalid XML`: parser notifies user with a wide range of messages whenever invalid syntax or some mistake
  was encountered in XML document.
  \
  Invalid XML example: https://feedforall.com/sample.xml
  \
  Its fragment (notice tags order):

      <i><font color="#0000FF">Homework Assignments <br> School Cancellations <br> Calendar of Events <br> Sports Scores <br> Clubs/Organization Meetings <br> Lunches Menus </i></font>
+ handling `commented pieces`: whenever commented piece like `<!-- wp:html -->` is encountered, it gets skipped.

## Tested RSS links

+ Channels like these are parsed correctly:

  http://rss.cnn.com/rss/edition.rss

  https://worldoftanks.ru/ru/rss/news/

  http://feeds.feedburner.com/welikedota


+ `curl's User-Agent` is used to access some RSS channels like this one:

  https://www.dotabuff.com/blog.rss


+ `<` char inside text is parsed correctly, as well as `commented pieces` are skipped properly:

  https://defenseofthepatience.libsyn.com/rss


+ `Empty XML document` is handled correctly:

  https://www.joindota.com/feeds/news


+ `Big channels` are parsed correctly:

  https://feeds.megaphone.fm/WWO3519750118

  https://feeds.simplecast.com/54nAGcIl


+ `CDATA` is parsed correctly:

  https://rss.art19.com/apology-line


+ User is notified if `invalid XML` is encountered:

  https://feedforall.com/sample.xml


+ Feeds in `Russian` are handled completely correctly:

  https://rss.dw.com/xml/rss-ru-rus

  https://people.onliner.by/feed

  https://brestcity.com/blog/feed

  https://rss.dw.com/xml/rss-ru-news

  https://lenta.ru/rss/top7

  https://www.liga.net/tech/battles/rss.xml

  https://vse.sale/news/rss


+ Some others:

  https://news.yahoo.com/rss/

  https://www.liquiddota.com/rss/news.xml


+ Please, see `Known problems` section below:

  https://www.theguardian.com/international/rss

  https://www.hyprgame.com/blog/category/dota2/feed/

## Testing

Modules tested:

+ _caching.py
+ _builder.py
+ _parser.py

Test coverage is 51%.

In order to run tests, please, install dependencies:

    pip install pytest pytest-cov

Then, provided, `/Homework/MarkKanaplianik/final_task` is your current directory, please, use the following command:

    pytest --cov=rss_news_reader tests/

## Known problems:

+ Some problems with PDF conversion exist:

    + https://www.theguardian.com/international/rss error saving to .pdf; this error happens because
      feature `-pdf-word-wrap: CJK;` is being used inside `.jinja2` template; without using this feature long strings
      are not wrapped on the next line;

    + https://www.hyprgame.com/blog/category/dota2/feed/ error saving to .pdf (for some reason FileNotFoundError is
      raised
      (No such file or directory), but both of them exist).

+ Big feeds like this one https://feeds.megaphone.fm/WWO3519750118 may get truncated when printing to console because of
  console's chars amount native limitations;

+ `--colorize` works console-specifically, which implies that in different terminals colorized text may look
  differently.
