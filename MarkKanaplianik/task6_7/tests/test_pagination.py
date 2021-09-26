import pytest

from MarkKanaplianik.task6_7.pagination.pagination import PageMissingError, Pagination


@pytest.fixture()
def pagination_your_beautiful_text_psize_5():
    return Pagination("Your beautiful text", page_size=5)


def test_pagination_arrange_on_pages(pagination_your_beautiful_text_psize_5):
    expected = ["Your ", "beaut", "iful ", "text"]
    actual = [page.text for page in pagination_your_beautiful_text_psize_5.pages]

    assert expected == actual


def test_pagination_page_count_after_arranging_on_pages(pagination_your_beautiful_text_psize_5):
    expected = 4
    actual = pagination_your_beautiful_text_psize_5.page_count

    assert expected == actual


def test_pagination_item_count_after_arranging_on_pages(pagination_your_beautiful_text_psize_5):
    expected = 19
    actual = pagination_your_beautiful_text_psize_5.item_count

    assert expected == actual


def test_pagination_rearrange_on_pages_after_page_size_change_on_3(pagination_your_beautiful_text_psize_5):
    expected = ["You", "r b", "eau", "tif", "ul ", "tex", "t"]
    pagination_your_beautiful_text_psize_5.page_size = 3
    actual = [page.text for page in pagination_your_beautiful_text_psize_5.pages]

    assert expected == actual


def test_pagination_page_count_after_page_size_change_on_3(pagination_your_beautiful_text_psize_5):
    expected = 7
    pagination_your_beautiful_text_psize_5.page_size = 3
    actual = pagination_your_beautiful_text_psize_5.page_count

    assert expected == actual


def test_pagination_rearrange_on_pages_after_text_change_on_hello_world(pagination_your_beautiful_text_psize_5):
    expected = ["Hello", " Worl", "d"]
    pagination_your_beautiful_text_psize_5.text = "Hello World"
    actual = [page.text for page in pagination_your_beautiful_text_psize_5.pages]

    assert expected == actual


def test_pagination_item_count_after_text_change_on_hello_world(pagination_your_beautiful_text_psize_5):
    expected = 11
    pagination_your_beautiful_text_psize_5.text = "Hello World"
    actual = pagination_your_beautiful_text_psize_5.item_count

    assert expected == actual


def test_pagination_count_items_on_page_valid_index(pagination_your_beautiful_text_psize_5):
    expected = 4
    actual = pagination_your_beautiful_text_psize_5.count_items_on_page(3)

    assert expected == actual


def test_pagination_count_items_on_page_invalid_index(pagination_your_beautiful_text_psize_5):
    with pytest.raises(PageMissingError):
        pagination_your_beautiful_text_psize_5.count_items_on_page(10)


def test_pagination_find_pages_where_text_completely_on_page(pagination_your_beautiful_text_psize_5):
    expected = [0]
    actual = pagination_your_beautiful_text_psize_5.find_page("Your")

    assert expected == actual


def test_pagination_find_pages_where_text_splitted_on_pages(pagination_your_beautiful_text_psize_5):
    expected = [1, 2]
    actual = pagination_your_beautiful_text_psize_5.find_page("beautiful")

    assert expected == actual


def test_pagination_set_page_size_not_positive_integer(pagination_your_beautiful_text_psize_5):
    with pytest.raises(ValueError):
        pagination_your_beautiful_text_psize_5.page_size = -1


def test_pagination_set_text_not_string(pagination_your_beautiful_text_psize_5):
    with pytest.raises(ValueError):
        pagination_your_beautiful_text_psize_5.text = 1
