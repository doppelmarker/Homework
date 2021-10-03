from collections import deque

from rss_reader.xml_parser.tokenizer import Tokenizer, TokenType, XMLError


class EmptyXMLDocumentError(XMLError):
    pass


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
                    elementStack[-1].children.append(token)
                    token.parent = elementStack[-1]

            if len(elementStack) != 0:
                return elementStack.pop()
            else:
                raise EmptyXMLDocumentError("empty xml document")
        except XMLError:
            pass
        finally:
            tokenizer.xml.close()
