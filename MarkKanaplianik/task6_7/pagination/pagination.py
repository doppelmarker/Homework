"""
Module provides Pagination class.
"""
import re
from math import ceil, floor


class PageMissingError(Exception):
    """Raised if page is not found."""

    pass


class TextMissingError(Exception):
    """Raised if text is not found on the pages."""

    pass


class Page:
    """Class to represent a page in the pagination."""

    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError(f"text has to be a string!")
        self._text = value

    def __len__(self):
        return len(self._text)

    def __str__(self):
        return self._text


class Pagination:
    """Class offering functionality of arranging text on pages and listing content on the given page.

    Supports iterator protocol.

    Text and page_size of the pagination can be modified through text and page_size properties. When altering these
    properties, pagination's pages get rearranged.

    Methods
    -------
    _update_pagination(text, page_size):
        Private method which updates the state of pagination when
        either __init__ is called or page_size and text properties are set new values
    count_items_on_page(page_index):
        Returns the amount of symbols on the page specified by page_index
    display_page(page_index):
        Returns the text on the page specified by page_index
    find_page(text):
        Returns the list of pages' indexes which contain text. If text is splitted in several lines, then indexes of all
        pages which partly contain the text are added to the resulting list
    """

    def __init__(self, text, *, page_size):
        self._update_pagination(text, page_size)
        self._text = text
        self._page_size = page_size

    def _update_pagination(self, text, page_size):
        len_text = len(text)
        pages_amount = ceil(len_text / page_size)
        pages = [Page(text[n * page_size : n * page_size + page_size]) for n in range(pages_amount)]
        self.pages = pages
        self.page_count = pages_amount
        self.item_count = len_text

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"page_size has to be a positive integer!")
        self._page_size = value
        self._update_pagination(self._text, value)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError(f"text has to be a string!")
        self._text = value
        self._update_pagination(value, self._page_size)

    def count_items_on_page(self, page_index):
        return len(self[page_index])

    def display_page(self, page_index):
        return str(self[page_index])

    def find_page(self, text):
        search_results = []
        occurrences = [m.start() for m in re.finditer(text, self._text)]
        page_size = self._page_size
        for occurrence in occurrences:
            start_page = floor(occurrence / page_size)
            end_page = floor((occurrence + len(text) - 1) / page_size)
            for n in range(start_page, end_page + 1):
                if n not in search_results:
                    search_results.append(n)
        if not search_results:
            raise TextMissingError(f"'{text}' is missing on the pages.")
        return search_results

    def __getitem__(self, page_index):
        try:
            return self.pages[page_index]
        except IndexError as e:
            raise PageMissingError(f"Invalid index. Page {page_index + 1} is missing.") from e

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i < len(self.pages):
            next_page = self.pages[self._i]
            self._i += 1
            return next_page
        else:
            raise StopIteration


def main():
    help(Pagination)

    pagination = Pagination("Your beautiful text", page_size=5)
    print(pagination.page_count)
    print(pagination.item_count)
    print(pagination.count_items_on_page(0))
    print(pagination.count_items_on_page(3))
    print(pagination.find_page("Your"))

    for page in pagination:
        print(page)

    print()

    pagination.text = "Kojima is genius!"
    print(pagination.page_count)
    print(pagination.item_count)
    print(pagination.count_items_on_page(0))
    print(pagination.count_items_on_page(3))
    print(pagination.find_page("i"))
    print()
    pagination.page_size = 3
    print(pagination.page_count)
    print(pagination.item_count)
    print(pagination.count_items_on_page(0))
    print(pagination.count_items_on_page(5))
    print(pagination.find_page("i"))


if __name__ == "__main__":
    main()
