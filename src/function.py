# Author: James Haller

from mybin import Bin
import logging

log = logging.getLogger('des-sim')

E = \
   [32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1]

S_BOXES = [
    # S_1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],

    # S_2
    [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
        [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]
    ],

    # S_3
    [
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
        [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
        [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
        [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]
    ],

    # S_4
    [
        [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
        [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
        [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
        [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]
    ],

    # S_5
    [
        [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
        [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
        [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
        [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]
    ],

    # S_6
    [
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
        [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
        [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
        [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]
    ],

    # S_7
    [
        [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
        [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
        [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
        [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]
    ],

    # S_8
    [
        [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
        [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
        [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
        [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]
    ]
]

P = \
   [16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25]


class Function:
    """
    GoF Context class
    """

    __slots__ = ['_encrypter', '_step', 'data', '_key', '_key_scheduler']

    def __init__(self, encrypter: 'Encrypter', key_scheduler: 'KeyScheduler'):
        self._encrypter = encrypter
        self._step = None
        self.data = None
        self._key = None
        self._key_scheduler = key_scheduler

    def get_result(self):
        self._step = Initialize(self)

        while self._step is not None:
            self._step = self._step.run()

        return self.data

    def set_new_data(self):
        self.data = self._encrypter.plaintext[1]

    def set_new_key(self):
        key = self._key_scheduler.get_key()
        log.info('        key output {} ({} bits)'.format(key, len(key)))
        self._key = key

    def _get_data(self):
        return self.data

    def _get_key(self):
        return self._key

    key = property(fget=_get_key)


"""=============================================================================="""


class FunctionStep:
    """
    GoF State super-class.
    """
    __slots__ = ['_context']

    def __init__(self, context: Function):
        self._context = context

    def run(self):
        raise NotImplementedError

    def _get_encrypter(self):
        return self._context._encrypter


class Initialize(FunctionStep):
    def run(self):
        log.info('    Starting f function...')
        self._context.set_new_data()
        self._context.set_new_key()
        return Expansion(self._context)


class Expansion(FunctionStep):
    OUTPUT_LEN = 48

    def run(self):
        s = ''
        for new_bit_loc in range(self.OUTPUT_LEN):
            old_bit_loc = E[new_bit_loc]
            s += str(self._context.data[old_bit_loc - 1])  # Must subtract 1 b/c PC tables are 1-indexed
        self._context.data = Bin(self.OUTPUT_LEN, s, 2)
        log.debug('        E result   {} ({} bits)'.format(self._context.data, len(self._context.data)))

        return Xor(self._context)


class Xor(FunctionStep):
    def run(self):
        self._context.data ^= self._context.key
        log.debug('        Xor result {} ({} bits)'.format(self._context.data, len(self._context.data)))
        return Split(self._context)


class Split(FunctionStep):
    def run(self):
        self._context.data = self._context.data.split(len(S_BOXES))

        log.debug('        Split for S boxes:')
        i = 1
        for s_in in self._context.data:
            log.debug('            [{}] {} ({} bits)'.format(i, s_in, len(s_in)))
            i += 1

        return SBoxes(self._context)


class SBoxes(FunctionStep):
    OUTPUT_LEN = 4

    def run(self):
        log.debug('        S box results:')

        data_lst = self._context.data
        for s_box_idx in range(len(S_BOXES)):
            s_box = S_BOXES[s_box_idx]
            data = data_lst[s_box_idx]

            row_idx = int(data[0] + data[len(data) - 1], 2)
            col_idx = int(data[1:len(data) - 1], 2)

            b = Bin(self.OUTPUT_LEN, s_box[row_idx][col_idx])
            data_lst[s_box_idx] = b

            log.debug('            [{}] {} ({} bits)'.format(s_box_idx + 1, b, len(b)))

        self._context.data = tuple(data_lst)

        return Recombine(self._context)


class Recombine(FunctionStep):
    def run(self):
        new_data = None
        for b in self._context.data:
            new_data = b if new_data is None else new_data + b
        self._context.data = new_data

        log.debug('        S box result {} ({} bits)'.format(self._context.data, len(self._context.data)))

        return Permutation(self._context)


class Permutation(FunctionStep):
    OUTPUT_LEN = 32

    def run(self):
        s = ''
        for new_bit_loc in range(self.OUTPUT_LEN):
            old_bit_loc = P[new_bit_loc]
            s += self._context.data[old_bit_loc - 1]  # Must subtract 1 b/c PC tables are 1-indexed
        self._context.data = Bin(self.OUTPUT_LEN, s, 2)

        log.debug('        P result {} ({} bits)'.format(self._context.data, len(self._context.data)))

        return None


from encrypter import *
