import pytest

from rss_reader.rss_builder import Feed, Item, RSSBuilder
from rss_reader.xml_parser import Attribute, Element


@pytest.fixture
def expected_feed():
    item1 = Item(
        id=1,
        title="",
        description="item1_description",
        link="",
        author="",
        pubDate="",
        links={"images": [], "audios": [], "others": []},
    )
    item2 = Item(
        id=2,
        title="",
        description="item2_description",
        link="",
        author="",
        pubDate="",
        links={"images": [], "audios": [], "others": []},
    )

    return Feed(
        title="title_text",
        description="description_text",
        link="link_text",
        image="",
        language="",
        items=[item1, item2],
    )


@pytest.fixture
def sample_attrs():
    return [
        Attribute(name="attr1", value="val1"),
        Attribute(name="attr2", value="val2"),
    ]


@pytest.fixture
def add_item():
    def _add_item(elem: Element, item_description: str):
        item1 = Element(tag_name="item", parent=elem, text="")

        item1_desc = Element(tag_name="description", parent=item1, text="")

        item1_desc_text = Element(
            tag_name=None, parent=item1_desc, text=item_description
        )

        item1_desc.children.append(item1_desc_text)

        item1.children.append(item1_desc)

        elem.children.append(item1)

    return _add_item


@pytest.fixture
def add_tag():
    def _add_tag(elem: Element, *, tag_name: str, tag_text: str):
        tag = Element(tag_name=tag_name, parent=elem, text="")

        tag_text_elem = Element(tag_name=None, parent=tag, text=tag_text)

        tag.children.append(tag_text_elem)

        elem.children.append(tag)

    return _add_tag


@pytest.fixture
def sample_dom(sample_attrs, add_item, add_tag):
    Element.update_forward_refs()
    rss = Element(tag_name="rss", attributes=sample_attrs, text="")
    channel = Element(tag_name="channel", parent=rss, text="")
    rss.children.append(channel)

    add_tag(channel, tag_name="title", tag_text="title_text")
    add_tag(channel, tag_name="description", tag_text="description_text")
    add_tag(channel, tag_name="link", tag_text="link_text")

    add_item(channel, "item1_description")
    add_item(channel, "item2_description")

    return rss


def test_build_feed(expected_feed, sample_dom):
    builder = RSSBuilder(sample_dom, 2, False)

    actual_feed = builder.build_feed()

    assert expected_feed == actual_feed
