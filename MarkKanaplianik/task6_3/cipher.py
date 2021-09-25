"""
Module provides Cipher class which possesses the functionality of Keyword encoding for latin alphabet.

Class:
    Cipher
"""
import string

from bidict import bidict


def bidirectional_letter_transformer(text, cipher_dict):
    """Helper generator function to perform encoding of a letter and vice versa."""

    for letter in text:
        encoded_letter = cipher_dict.get(letter.lower(), letter)
        if letter.isupper():
            encoded_letter = encoded_letter.upper()
        yield encoded_letter


class Cipher:
    """Class to encode and decode text according to keyword cipher.

    Cipher class utilizes bidict from bidict package in order to easily perform encoding and decoding operations.

    Methods
    -------
    encode(text):
        Encode text
    decode(text):
        Decode text
    """

    def __init__(self, *, keyword="crypto"):
        alphabet = string.ascii_lowercase
        filtered_alphabet = "".join(filter(lambda letter: letter not in keyword, alphabet))
        cipher_alphabet = keyword + filtered_alphabet
        cipher_dict = bidict({l1: l2 for l1, l2 in zip(alphabet, cipher_alphabet)})
        self._cipher_dict = cipher_dict

    def encode(self, text):
        return "".join(bidirectional_letter_transformer(text, self._cipher_dict))

    def decode(self, text):
        return "".join(bidirectional_letter_transformer(text, self._cipher_dict.inverse))


def main():
    cipher = Cipher()
    print(cipher.encode("Hello world"))
    print(cipher.decode("Fjedhc dn atidsn"))


if __name__ == "__main__":
    main()
