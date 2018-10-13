# Author: James Haller


class Encrypter:
    __slots__ = ['_plaintext', '_ciphertext']

    def __init__(self, plaintext):
        self._plaintext = plaintext
        self._ciphertext = self._plaintext
