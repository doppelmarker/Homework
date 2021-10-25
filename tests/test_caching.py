import json
import os
from pathlib import Path

import pytest

from rss_reader.reader import NewsCache, NewsNotFoundError
from rss_reader.rss_builder import Feed, Item

EMPTY_FILE_NAME = "empty_tested_cache.json"
COMPLETE_FILE_NAME = "complete_tested_cache.json"
DAMAGED_FILE_NAME = "damaged_tested_cache.json"
NO_HEAD_FILE_NAME = "no_head_cache.json"
NO_SOURCE_FILE_NAME = "no_source_cache.json"
RANDOM_FILE_NAME = "random_file_name.json"


@pytest.fixture
def sample_items():
    return [
        Item(id=1, title="Item1", pubDate="2021-10-23T15:08:00Z"),
        Item(id=2, title="Item2", pubDate="2021-10-23T15:08:00Z"),
    ]


@pytest.fixture
def sample_feed(sample_items):
    return Feed(
        title="Cool story",
        description="Once upon a time...",
        link="https://google.com",
        items=sample_items,
    )


@pytest.fixture
def expected_complete_cache_content(sample_feed):
    rss = "https://news.yahoo.com/rss/"
    json_dict = {rss: []}
    json_dict[rss].append(sample_feed.dict(exclude={"items"}))
    for item in sample_feed.items:
        json_dict[rss].append(item.dict())
    return json.dumps(json_dict, indent=4, ensure_ascii=False)


@pytest.fixture
def no_head_file_content(sample_feed):
    rss = "https://news.yahoo.com/rss/"
    json_dict = {rss: []}
    for item in sample_feed.items:
        json_dict[rss].append(item.dict())
    return json.dumps(json_dict, indent=4, ensure_ascii=False)


@pytest.fixture
def other_source_file_content(sample_feed):
    other_rss = "https://some_other_source/"
    rss = "https://news.yahoo.com/rss/"
    json_dict = {other_rss: [], rss: []}
    json_dict[rss].append(sample_feed.dict(exclude={"items"}))
    for item in sample_feed.items:
        json_dict[rss].append(item.dict())
    return json.dumps(json_dict, indent=4, ensure_ascii=False)


@pytest.fixture
def empty_cache_file():
    cache = open(EMPTY_FILE_NAME, "w+")
    yield cache
    cache.close()


@pytest.fixture
def complete_cache_file(expected_complete_cache_content):
    cache = open(COMPLETE_FILE_NAME, "w+")
    cache.write(expected_complete_cache_content)
    cache.seek(0)
    yield cache
    cache.close()


@pytest.fixture
def damaged_cache_file():
    cache = open(DAMAGED_FILE_NAME, "w+")
    cache.write(".,.:,.,.}{")
    cache.seek(0)
    yield cache
    cache.close()


@pytest.fixture
def no_head_cache_file(no_head_file_content):
    cache = open(NO_HEAD_FILE_NAME, "w+")
    cache.write(no_head_file_content)
    cache.seek(0)
    yield cache
    cache.close()


@pytest.fixture
def no_source_cache_file():
    cache = open(NO_SOURCE_FILE_NAME, "w+")
    cache.write(
        """{
    "https://some_other_source/": []
}"""
    )
    cache.seek(0)
    yield cache
    cache.close()


@pytest.fixture(scope="module")
def bare_cache_obj():
    return NewsCache(Path(), "")


@pytest.fixture(scope="module")
def cache_obj():
    return NewsCache(Path(EMPTY_FILE_NAME), "https://news.yahoo.com/rss/")


@pytest.fixture(scope="module")
def damaged_cache_obj():
    return NewsCache(Path(DAMAGED_FILE_NAME), "https://news.yahoo.com/rss/")


@pytest.mark.parametrize(
    "test_date_format, parsed_date",
    [
        ["2021-10-22T15:08:00Z", "20211022"],
        ["Fri, 9 Sep 2021 15:12:17 -0000", "20210909"],
        ["Tue, 12 Oct 2021 14:54:09 GMT", "20211012"],
    ],
)
def test_get_parsed_date_from_datetime_obj_positive(
    bare_cache_obj, test_date_format, parsed_date
):
    datetime_obj = bare_cache_obj._get_datetime_obj(test_date_format)
    assert (
        f"{datetime_obj.year}{datetime_obj.month:02d}{datetime_obj.day:02d}"
        == parsed_date
    )


def test_get_datetime_obj_raises_ValueError_if_invalid_date(bare_cache_obj):
    invalid_date = "Thursday 4th 4444"
    with pytest.raises(ValueError):
        bare_cache_obj._get_datetime_obj(invalid_date)


def test_cache_news_path_raises_FileNotFoundError_if_no_file(sample_feed):
    with pytest.raises(FileNotFoundError):
        NewsCache(Path(RANDOM_FILE_NAME), "").cache_news(sample_feed)


def test_cache_news_empty_cache(
    cache_obj, sample_feed, empty_cache_file, expected_complete_cache_content
):
    cache_obj.cache_news(sample_feed)
    empty_cache_file.seek(0)
    assert expected_complete_cache_content == empty_cache_file.read()
    empty_cache_file.close()
    os.remove(EMPTY_FILE_NAME)


def test_cache_news_complete_cache(
    sample_feed, complete_cache_file, expected_complete_cache_content
):
    """Nothing should change in cache file, if already cached news is similar to one which is going to be cached."""

    NewsCache(
        Path("complete_tested_cache.json"), "https://news.yahoo.com/rss/"
    ).cache_news(sample_feed)
    complete_cache_file.seek(0)
    assert expected_complete_cache_content == complete_cache_file.read()
    complete_cache_file.close()
    os.remove(COMPLETE_FILE_NAME)


def test_cache_news_damaged_cache(
    damaged_cache_obj, sample_feed, damaged_cache_file, expected_complete_cache_content
):
    damaged_cache_obj.cache_news(sample_feed)
    damaged_cache_file.seek(0)
    assert expected_complete_cache_content == damaged_cache_file.read()
    damaged_cache_file.close()
    os.remove(DAMAGED_FILE_NAME)


def test_cache_news_no_head_in_cache(
    sample_feed, no_head_cache_file, expected_complete_cache_content
):
    NewsCache(Path(NO_HEAD_FILE_NAME), "https://news.yahoo.com/rss/").cache_news(
        sample_feed
    )
    no_head_cache_file.seek(0)
    assert expected_complete_cache_content == no_head_cache_file.read()
    no_head_cache_file.close()
    os.remove(NO_HEAD_FILE_NAME)


def test_cache_news_no_source(
    sample_feed,
    no_source_cache_file,
    expected_complete_cache_content,
    other_source_file_content,
):
    NewsCache(Path(NO_SOURCE_FILE_NAME), "https://news.yahoo.com/rss/").cache_news(
        sample_feed
    )
    no_source_cache_file.seek(0)
    assert other_source_file_content == no_source_cache_file.read()
    no_source_cache_file.close()
    os.remove(NO_SOURCE_FILE_NAME)


def test_get_cached_news_raises_FileNotFoundError_if_no_file():
    with pytest.raises(FileNotFoundError):
        NewsCache(Path(RANDOM_FILE_NAME), "").get_cached_news("any date", 1)


def test_get_cached_news_raises_NewsNotFoundError_if_empty_cache(
    cache_obj, empty_cache_file
):
    with pytest.raises(NewsNotFoundError):
        cache_obj.get_cached_news("any date", 1)
    empty_cache_file.close()
    os.remove(EMPTY_FILE_NAME)


def test_get_cached_news_raises_NewsNotFoundError_if_damaged_cache(
    damaged_cache_obj, damaged_cache_file
):
    with pytest.raises(NewsNotFoundError):
        damaged_cache_obj.get_cached_news("any date", 1)
    damaged_cache_file.close()
    os.remove(DAMAGED_FILE_NAME)


def test_get_cached_news_all_items_with_specified_date(
    complete_cache_file, sample_feed, expected_complete_cache_content
):
    cache = NewsCache(Path(COMPLETE_FILE_NAME), "https://news.yahoo.com/rss/")

    actual_feed = cache.get_cached_news("20211023", 2)[0]

    assert sample_feed == actual_feed


def test_get_cached_news_no_news_found_with_specified_date_raises_NoNewsFoundError(
    complete_cache_file, expected_complete_cache_content
):
    cache = NewsCache(Path(COMPLETE_FILE_NAME), "https://news.yahoo.com/rss/")

    with pytest.raises(NewsNotFoundError):
        cache.get_cached_news("20211024", 2)
    complete_cache_file.close()
    os.remove(COMPLETE_FILE_NAME)
