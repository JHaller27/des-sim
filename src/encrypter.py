# Author: James Haller
from function import Function
from key_scheduler import KeyScheduler
from typing import Union
from mybin import Bin
import logging

log = logging.getLogger('des-sim')

L, R = 0, 1

IP = \
    [58, 50, 42, 34, 26, 18, 10, 2,
     60, 52, 44, 36, 28, 20, 12, 4,
     62, 54, 46, 38, 30, 22, 14, 6,
     64, 56, 48, 40, 32, 24, 16, 8,
     57, 49, 41, 33, 25, 17, 9, 1,
     59, 51, 43, 35, 27, 19, 11, 3,
     61, 53, 45, 37, 29, 21, 13, 5,
     63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = \
    [40, 8, 48, 16, 56, 24, 64, 32,
     39, 7, 47, 15, 55, 23, 63, 31,
     38, 6, 46, 14, 54, 22, 62, 30,
     37, 5, 45, 13, 53, 21, 61, 29,
     36, 4, 44, 12, 52, 20, 60, 28,
     35, 3, 43, 11, 51, 19, 59, 27,
     34, 2, 42, 10, 50, 18, 58, 26,
     33, 1, 41, 9, 49, 17, 57, 25]


class Encrypter:
    __slots__ = ['plaintext', 'ciphertext', 'f', '_key_scheduler', '_step']

    BLOCKSIZE = 64
    NUM_ROUNDS = 16

    def __init__(self, key_scheduler: KeyScheduler):
        self.plaintext = None
        self.ciphertext = None
        self.f = Function(self)
        self._key_scheduler = key_scheduler
        self._step = None

    def get_key(self):
        key = self._key_scheduler.get_key()
        log.info('        key output {} ({} bits)'.format(key, len(key)))
        return key

    def encrypt(self, plaintext: Union[Bin, str]):
        """
        Encrypt a binary plaintext using DES
        :param plaintext: String representation of a binary message
        :return: Encrypted message, ie the ciphertext
        """
        from math import ceil

        if isinstance(plaintext, str):
            plaintext = Bin(Bin.INF, plaintext)
        self.ciphertext = None

        # Get list of blocks to encrypt
        blk_lst = []
        num_blocks = ceil(len(plaintext) / self.BLOCKSIZE)

        for i in range(num_blocks):
            blk = str(plaintext)[i * self.BLOCKSIZE:(i + 1) * self.BLOCKSIZE]

            # Pad out to BLOCKSIZE
            while len(blk) < self.BLOCKSIZE:
                blk += '0'
            blk = '0b' + blk

            blk_lst.append(Bin(self.BLOCKSIZE, blk))

        # Encrypt each block
        result_ciphertext = None
        for blk in blk_lst:
            log.info('\nEncrypting block {} ({} bits)'.format(blk, len(blk)))
            self._encrypt_one(blk)
            result_ciphertext = self.ciphertext if result_ciphertext is None else result_ciphertext + self.ciphertext

        return str(result_ciphertext)

    def _encrypt_one(self, blk: Bin):
        self.plaintext = blk

        self._step = Initialize(self)
        self.run()
        log.info('    Result L_0 = {} ({} bits)\n'
                 '           R_0 = {} ({} bits)'.format(self.plaintext[0], len(self.plaintext[0]),
                                                        self.plaintext[1], len(self.plaintext[1])))

        for round_num in range(1, self.NUM_ROUNDS + 1):
            log.info('\nEnter round {}...'.format(round_num))
            self._step = StartRound(self)
            self.run()
            log.info('    Result L_{} = {} ({} bits)\n'
                     '           R_{} = {} ({} bits)'.format(round_num, self.plaintext[L], len(self.plaintext[L]),
                                                             round_num, self.plaintext[R], len(self.plaintext[R])))

        self._step = BeginEnd(self)
        self.run()
        log.info('Encrypted block = {} ({} bits)\n'.format(self.ciphertext, len(self.ciphertext)))

    def run(self):
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
        log.info('Initializing encryption machine')
        return InitialPermutation(self._encrypter)


class InitialPermutation(RoundStep):
    OUTPUT_LEN = 64

    def run(self):
        s = ''
        for new_bit_loc in range(self.OUTPUT_LEN):
            old_bit_loc = IP[new_bit_loc]
            s += str(self._encrypter.plaintext[old_bit_loc - 1])  # Must subtract 1 b/c IP tables are 1-indexed
        self._encrypter.plaintext = Bin(self.OUTPUT_LEN, s, 2).split(2)

        return None


"""=============================================================================="""


class StartRound(RoundStep):
    def run(self):
        return Xor(self._encrypter)


class Xor(RoundStep):
    def run(self):
        f_result = self._encrypter.f.get_result()
        log.info('    f output = {} ({} bits)'.format(f_result, len(f_result)))
        self._encrypter.plaintext[L] ^= f_result
        log.debug('    f xor left {} ({} bits)'.format(self._encrypter.plaintext[L],
                                                       len(self._encrypter.plaintext[L])))
        return SwapSides(self._encrypter)


class SwapSides(RoundStep):
    def run(self):
        log.info('    swap left & right')
        self._encrypter.plaintext[L], self._encrypter.plaintext[R] = \
            self._encrypter.plaintext[R], self._encrypter.plaintext[L]
        return None


"""=============================================================================="""


class BeginEnd(RoundStep):
    def run(self):
        log.info('\nBegin end of encryption machine...')
        return LastSwap(self._encrypter)


class LastSwap(RoundStep):
    def run(self):
        self._encrypter.plaintext[L], self._encrypter.plaintext[R] = \
            self._encrypter.plaintext[R], self._encrypter.plaintext[L]
        return Recombine(self._encrypter)


class Recombine(RoundStep):
    def run(self):
        self._encrypter.plaintext = self._encrypter.plaintext[L] + self._encrypter.plaintext[R]
        return FinalPermutation(self._encrypter)


class FinalPermutation(RoundStep):
    OUTPUT_LEN = 64

    def run(self):
        s = ''
        for new_bit_loc in range(self.OUTPUT_LEN):
            old_bit_loc = IP_INV[new_bit_loc]
            s += self._encrypter.plaintext[old_bit_loc - 1]  # Must subtract 1 b/c IP tables are 1-indexed
        self._encrypter.ciphertext = Bin(self.OUTPUT_LEN, s, 2)

        return None
