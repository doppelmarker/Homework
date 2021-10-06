import logging
from collections import deque

from rss_reader.xml_parser.tokenizer import Tokenizer, TokenType, XMLError

logger = logging.getLogger("rss-reader")


class Parser:
    def __init__(self, xml):
        self.xml = xml

    def parse(self):
        tokenizer = Tokenizer(self.xml)
        try:
            elementStack = deque()

            for token in tokenizer:
                if tokenizer.token_type == TokenType.START_TAG:
                    if len(elementStack) != 0:
                        elementStack[-1].children.append(token)
                        token.parent = elementStack[-1]
                    elementStack.append(token)
                elif tokenizer.token_type == TokenType.END_TAG:
                    if len(elementStack) > 1:
                        elementStack.pop()
                elif tokenizer.token_type == TokenType.TEXT:
                    if not tokenizer.text.isspace():
                        elementStack[-1].children.append(token)
                        token.parent = elementStack[-1]

            return elementStack.pop()
        finally:
            tokenizer.xml_io.close()
