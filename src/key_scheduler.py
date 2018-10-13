# Author: James Haller

"""
Uses Gang-of-Four State pattern to retrieve DES keys **in order**.
"""
from mybin import Bin

PC1 = [57, 49, 41, 33, 25, 17,  9,  1,
       58, 50, 42, 34, 26, 18, 10,  2,
       59, 51, 43, 35, 27, 19, 11,  3,
       60, 52, 44, 36, 63, 55, 47, 39,
       31, 23, 15,  7, 62, 54, 46, 38,
       30, 22, 14,  6, 61, 53, 45, 37,
       29, 21, 13,  5, 28, 20, 12,  4]

PC2 = [14, 17, 11, 24,  1,  5,  3, 28,
       15,  6, 21, 10, 23, 19, 12,  4,
       26,  8, 16,  7, 27, 20, 13,  2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

SINGLE_BIT_SHIFT_ROUNDS = [1, 2, 9, 16]


class KeyScheduler:
    """
    GoF Context class.
    """
    __slots__ = ['_original_key', '_step', '_round_num', 'key', 'C', 'D']

    def __init__(self, key):
        if not isinstance(key, Bin):
            key = Bin(64, key)

        assert len(key) == 64
        self._original_key = key
        self.key = self._original_key

        self._round_num = 0

        self._step = Initialization(self)
        self._transform()  # Run Initialization step

    def _transform(self):
        while self._step is not None:
            self._step = self._step.run()

    def _get_round_num(self):
        return self._round_num

    def get_key(self):
        self._step = TransformStart(self)
        self._transform()
        return self.key

    def next_round(self):
        self._round_num += 1

    round = property(fget=_get_round_num)


"""=============================================================================="""


class RoundStep:
    """
    GoF State super-class.
    """
    __slots__ = ['_scheduler']

    def __init__(self, scheduler):
        self._scheduler = scheduler

    def run(self):
        raise NotImplementedError


class Initialization(RoundStep):
    KEY_OUTPUT_LEN = 56

    def run(self):
        s = ''
        for new_bit_loc in range(self.KEY_OUTPUT_LEN):
            old_bit_loc = PC1[new_bit_loc]
            s += str(self._scheduler.key[old_bit_loc - 1])  # Must subtract 1 b/c PC tables are 1-indexed
        self._scheduler.C, self._scheduler.D = Bin(self.KEY_OUTPUT_LEN, s, 2).split(2)

        return None


class TransformStart(RoundStep):
    def run(self):
        return Rotate(self._scheduler)


class Rotate(RoundStep):
    def run(self):
        assert isinstance(self._scheduler.C, Bin)
        assert isinstance(self._scheduler.D, Bin)

        self._scheduler.next_round()

        shift = 1 if self._scheduler.round in SINGLE_BIT_SHIFT_ROUNDS else 2

        self._scheduler.C << shift
        self._scheduler.D << shift

        return Permute(self._scheduler)


class Permute(RoundStep):
    KEY_OUTPUT_LEN = 48

    def run(self):
        assert isinstance(self._scheduler.C, Bin)
        assert isinstance(self._scheduler.D, Bin)

        key = self._scheduler.C + self._scheduler.D

        s = ''
        for new_bit_loc in range(self.KEY_OUTPUT_LEN):
            old_bit_loc = PC2[new_bit_loc]
            s += str(self._scheduler.key[old_bit_loc - 1])  # Must subtract 1 b/c PC tables are 1-indexed

        self._scheduler.key = key

        return None
