# Author: James Haller

from key_scheduler import KeyScheduler
from mybin import Bin


class Encrypter:
    __slots__ = ['plaintext', 'ciphertext', '_key_scheduler']

    BLOCKSIZE = 64

    def __init__(self, key_scheduler: KeyScheduler):
        self.plaintext = None
        self.ciphertext = None
        self._key_scheduler = key_scheduler

    def get_key(self):
        return self._key_scheduler.get_key()

    def encrypt(self, plaintext: str):
        """
        Encrypt a binary plaintext using DES
        :param plaintext: String representation of a binary message
            (format: no leading '0b', all digits/characters must be in base 2)
        :return: Encrypted message, ie the ciphertext
        """
        from math import ceil

        self.ciphertext = None

        # Get list of blocks to encrypt
        blk_lst = []
        num_blocks = ceil(len(plaintext) / self.BLOCKSIZE)

        for i in range(num_blocks):
            blk = plaintext[i * self.BLOCKSIZE:(i+1) * self.BLOCKSIZE]

            # Pad out to BLOCKSIZE
            while len(blk) < self.BLOCKSIZE:
                blk += '0'

            blk_lst.append(Bin(self.BLOCKSIZE, blk, 2))

        # Encrypt each block
        for blk in blk_lst:
            self._encrypt_one(blk)

        return str(self.ciphertext)

    def _encrypt_one(self, blk):
        self.plaintext = blk
        self.ciphertext = self.plaintext if self.ciphertext is None else self.ciphertext + self.plaintext
