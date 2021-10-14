import logging
from collections import deque

from rss_reader.xml_parser.tokenizer import Tokenizer, TokenType, XMLError

logger = logging.getLogger("rss-reader")


class Parser:
    def __init__(self, xml):
        self.xml = xml

    def _tokenize(self, tokenizer, stack):
        try:
            for token in tokenizer:
                if tokenizer.token_type == TokenType.START_TAG:
                    if len(stack) != 0:
                        stack[-1].children.append(token)
                        token.parent = stack[-1]
                    stack.append(token)
                elif tokenizer.token_type == TokenType.END_TAG:
                    if len(stack) > 1:
                        try:
                            while stack.pop().tag_name != token.tag_name:
                                pass
                        except IndexError:
                            # issue with https://feedforall.com/sample.xml
                            raise XMLError("invalid xml")
                elif tokenizer.token_type == TokenType.TEXT:
                    if not tokenizer.text.isspace():
                        stack[-1].children.append(token)
                        token.parent = stack[-1]
                elif tokenizer.token_type == TokenType.CDATA:
                    self._tokenize(tokenizer.cdata_tokenizer, stack)
        finally:
            tokenizer.xml_io.close()

    def parse(self):
        tokenizer = Tokenizer(self.xml)

        element_stack = deque()

        logger.info("Start parsing RSS...")

        self._tokenize(tokenizer, element_stack)

        logger.info("Successfully parsed RSS document!")

        return element_stack.pop()
