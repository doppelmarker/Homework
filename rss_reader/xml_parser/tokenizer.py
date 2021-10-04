from enum import Enum
from io import StringIO

from rss_reader.xml_parser.parser_models import Attribute, Element


class TokenType(Enum):
    BOF = 1
    START_TAG = 2
    END_TAG = 3
    TEXT = 4
    EOF = 5


class XMLError(Exception):
    pass


class InvalidTagError(XMLError):
    pass


class UnexpectedCharacterError(XMLError):
    pass


class EmptyAttributeNameError(XMLError):
    pass


class InvalidAttributeError(XMLError):
    pass


class UnexpectedEndOfDocumentError(XMLError):
    pass


class Tokenizer:
    def __init__(self, xml):
        self.xml_io = StringIO(xml)
        self._skip_head()
        self.attributes = []
        self.token_type = TokenType.BOF
        self.text: str
        self.has_end_tag: bool = False
        self.tag_name: str

    def _skip_head(self):
        while _ := self._read_char() != ">":
            pass

    def _skip_tag(self):
        counter_left_bracket = 1
        counter_right_bracket = 0
        while counter_left_bracket != counter_right_bracket:
            char = self._read_char()
            if char == "<":
                counter_left_bracket += 1
            elif char == ">":
                counter_right_bracket += 1

    def __iter__(self):
        return self

    def __next__(self):
        self._next_token()
        if self.token_type == TokenType.START_TAG:
            return Element(
                tag_name=self.tag_name, attributes=self.attributes, text=self.text
            )
        elif self.token_type == TokenType.END_TAG:
            return Element(tag_name=self.tag_name)
        elif self.token_type == TokenType.TEXT:
            return Element(text=self.text)
        elif self.token_type == TokenType.EOF:
            raise StopIteration

    def _next_token(self):
        if self.token_type == TokenType.BOF:
            self._parse_text()

        if (
            self.token_type == TokenType.START_TAG
            or self.token_type == TokenType.END_TAG
        ):
            if self.has_end_tag:
                self._reset(False)
                self.token_type = TokenType.END_TAG
                self.has_end_tag = False
            else:
                self._reset(True)
                self._parse_text()
                if self.token_type == TokenType.TEXT and self.text == "":
                    self._reset(True)
                    self._parse_tag()
        elif self.token_type == TokenType.TEXT:
            self._reset(True)
            self._parse_tag()
        elif self.token_type == TokenType.EOF:
            pass

    def _reset(self, reset_tag_name):
        if reset_tag_name:
            self.tag_name = ""
        self.attributes.clear()
        self.text = ""

    def _match_next_char(self, expected, skip_ws):
        char = self._read_char(skip_ws)
        if char != expected:
            raise UnexpectedCharacterError(
                f"unexpected character: expected [{expected}], got [{char}]"
            )

    def _read_char(self, skip_ws=False):
        char = self.xml_io.read(1)
        if skip_ws:
            if char == "":
                raise UnexpectedEndOfDocumentError("unexpected end of document")
        while True:
            if char != "" and skip_ws and char.isspace():
                char = self.xml_io.read(1)
                continue
            return char

    def _parse_text(self):
        text = ""
        char = self._read_char()
        while char != "" and char != "<":
            text += char
            char = self._read_char()
        # if not end of xml
        if char != "":
            self.token_type = TokenType.TEXT
            self.text = text
        else:
            self.token_type = TokenType.EOF

    def _parse_tag(self):
        is_start_tag = True

        char = self._read_char()
        if char == "!" or char == "?":
            self._skip_tag()
            self._parse_text()
            return

        if char == "/":
            is_start_tag = False
            char = self._read_char()

        tag_name = ""
        while char.isalnum() or char == "-" or char == ":" or char == "?":
            tag_name += char
            char = self._read_char()

        self.tag_name = tag_name

        INVALID_TAG = f"invalid tag: <{'' if is_start_tag else '/'}{tag_name}>"

        if len(tag_name) == 0:
            raise InvalidTagError(INVALID_TAG)
        else:
            if is_start_tag:
                self.token_type = TokenType.START_TAG
                if char == ">":
                    pass
                elif char == "/":
                    self._match_next_char(">", False)
                    self.has_end_tag = True
                else:
                    if not char.isspace():
                        raise InvalidTagError(INVALID_TAG)
                    self.has_end_tag = self._parse_attrs()
            else:
                self.token_type = TokenType.END_TAG
                if char == ">":
                    pass
                else:
                    if not char.isspace():
                        raise InvalidTagError(INVALID_TAG)
                    self._match_next_char(">", True)

    def _parse_attrs(self):
        char = self._read_char(True)

        while char != ">":
            if char == "/":
                self._match_next_char(">", False)
                return True

            attr_name = ""

            while char.isalnum() or char == ":":
                attr_name += char
                char = self._read_char()

            if len(attr_name) == 0:
                raise EmptyAttributeNameError(
                    f"empty attribute name in tag: <{self.tag_name}>"
                )

            if char.isspace():
                char = self._read_char(True)

            if char != "=":
                raise InvalidAttributeError("invalid attribute" + str(self))

            char = self._read_char(True)
            if char != "'" and char != '"':
                raise InvalidAttributeError("invalid attribute" + str(self))

            delimiter = char

            char = self._read_char()

            attr_value = ""
            while char != delimiter:
                attr_value += char
                char = self._read_char()

            char = self._read_char(True)
            self.attributes.append(Attribute(name=attr_name, value=attr_value))

        return False

    def __str__(self):
        return f"<{self.tag_name} {self.attributes} {self.has_end_tag}>{self.text}"
