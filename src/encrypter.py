# Author: James Haller

from key_scheduler import KeyScheduler
from mybin import Bin


class Encrypter:
    __slots__ = ['plaintext', 'ciphertext', '_key_scheduler', '_step']

    BLOCKSIZE = 64

    def __init__(self, key_scheduler: KeyScheduler):
        self.plaintext = None
        self.ciphertext = None
        self._key_scheduler = key_scheduler
        self._step = None

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
        result_ciphertext = None
        for blk in blk_lst:
            self._encrypt_one(blk)
            result_ciphertext = self.ciphertext if result_ciphertext is None else result_ciphertext + self.ciphertext

        return str(result_ciphertext)

    def _encrypt_one(self, blk: Bin):
        self.plaintext = blk
        self._step = Initialize(self)

        while self._step is not None:
            self._step = self._step.run()


"""=============================================================================="""


class RoundStep:
    """
    GoF State super-class.
    """
    __slots__ = ['_encrypter']

    def __init__(self, encrypter: Encrypter):
        self._encrypter = encrypter

    def run(self):
        raise NotImplementedError


class Initialize(RoundStep):
    def run(self):
        return None
