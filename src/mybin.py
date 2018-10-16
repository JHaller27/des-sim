# Author: James Haller
from typing import Union


class Bin:
    __slots__ = ['_val', '_num_digits']

    INF = -1

    def copy(self):
        return Bin(self._num_digits, self._val)

    def ltrim(self, target):
        """
        Trim from left side by right-shifting (and dropping digits)
        :param target: Target number of digits
        :return: Shifted Bin object
        """
        shift_amt = self._num_digits - target
        x = self._val >> shift_amt
        return Bin(target, x)

    def rtrim(self, target):
        """
        Trim from right side by left-shifting (and dropping digits)
        :param target: Target number of digits
        :return: Shifted Bin object
        """
        shift_amt = self._num_digits - target
        x = self._val << shift_amt
        return Bin(target, x)

    def split(self, num: int):
        """
        Split this Bin into evenly-sized chunks
        :param num: Number of chunks to divide into
        :return: List of Bin objects of even length
        """
        assert len(self) % num == 0

        num_str = str(self)
        offset = len(self) // num
        return [Bin(offset, num_str[i * offset:(i + 1) * offset], 2) for i in range(num)]

    def __init__(self, num_digits: Union[int, 'Bin'], val: Union[int, str]=0, base: int=None):
        if isinstance(num_digits, Bin):
            self._num_digits = num_digits._num_digits
            self._val = num_digits._val
        else:
            self._num_digits = int(num_digits)

            if isinstance(val, str):
                val = val.lower()
                if base is None:
                    if val.startswith('0x'):
                        base = 16
                        val = val[2:]
                        if self._num_digits == self.INF:
                            self._num_digits = len(val) * 4  # 1 hex digit = 4 bits
                    elif val.startswith('0o'):
                        base = 8
                        val = val[2:]
                        if self._num_digits == self.INF:
                            self._num_digits = len(val) * 3  # 1 hex digit = 4 bits
                    elif val.startswith('0b'):
                        base = 2
                        val = val[2:]
                        if self._num_digits == self.INF:
                            self._num_digits = len(val)
                    else:
                        base = 10
                        if self._num_digits == self.INF:
                            self._num_digits = len('{:b}'.format(int(val)))
                self._val = int(val, base)
            else:
                self._val = int(val)

            if not 1 <= self._num_digits:
                raise ValueError('number of digits must be greater than or equal to 1')

    def __add__(self, other: 'Bin'):
        """
        Concatenate another Bin onto the end of this one
        :param other: Bin object for concatenation
        :return: This Bin with other Bin concatenated to right side
        """
        return Bin(len(self) + len(other), str(self) + str(other), 2)

    def __xor__(self, other):
        if isinstance(other, Bin):
            return Bin(self._num_digits, self._val.__xor__(Bin(other)._val))

    def __str__(self):
        return '{:0{}b}'.format(self._val, self._num_digits)

    def __int__(self):
        return self._val

    def __lshift__(self, other):
        x = int(self)

        if other > 0:
            for i in range(other):
                x <<= 1
                if x >= 2 ** self._num_digits - 1:
                    x -= 2 ** self._num_digits - 1
            return Bin(self._num_digits, x)
        elif other < 0:
            return self >> -other
        else:
            return self

    def __rshift__(self, other):
        x = int(self)

        if other > 0:
            for i in range(other):
                odd = x % 2 == 1
                x >>= 1
                if odd:
                    x += 2 ** self._num_digits - 1
            return Bin(x, self._num_digits)
        elif other < 0:
            return self << -other
        else:
            return self

    def __len__(self):
        return self._num_digits

    def __iter__(self):
        return [int(x) for x in str(self)]

    def __getitem__(self, index):
        return str(self)[index]
