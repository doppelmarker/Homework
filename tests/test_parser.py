import pytest

from rss_reader.xml_parser import Attribute, Element, Parser


@pytest.fixture
def common_xml_to_parse():
    return """
<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">
    <channel>
        <title>Yahoo News - Latest News & Headlines</title>
        <link>https://www.yahoo.com/news</link>
    </channel>
</rss>
"""


@pytest.fixture
def expected_attrs():
    return [
        Attribute(name="xmlns:media", value="http://search.yahoo.com/mrss/"),
        Attribute(name="version", value="2.0"),
    ]


@pytest.fixture
def add_tag():
    def _add_tag(elem: Element, *, tag_name: str, tag_text: str):
        tag = Element(tag_name=tag_name, parent=elem, text="")

        tag_text_elem = Element(tag_name=None, parent=tag, text=tag_text)

        tag.children.append(tag_text_elem)

        elem.children.append(tag)

    return _add_tag


@pytest.fixture
def expected_dom(expected_attrs, add_tag):
    Element.update_forward_refs()
    rss = Element(tag_name="rss", attributes=expected_attrs, text="")
    channel = Element(tag_name="channel", parent=rss, text="")
    rss.children.append(channel)

    add_tag(channel, tag_name="title", tag_text="Yahoo News - Latest News & Headlines")
    add_tag(channel, tag_name="link", tag_text="https://www.yahoo.com/news")

    return rss


def test_parser(common_xml_to_parse, expected_dom):
    parser = Parser(common_xml_to_parse)

    actual_dom = parser.parse()

    assert expected_dom == actual_dom
