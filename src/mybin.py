# Author: James Haller


class Bin:
    __slots__ = ['_val', '_num_digits']

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

    def extend(self, other: 'Bin'):
        """
        Concatenate another Bin onto the end of this one
        :param other: Bin object for concatenation
        :return: This Bin with other Bin concatenated to right side
        """
        return Bin(len(self) + len(other), str(self) + str(other), 2)

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

    def __init__(self, num_digits, val=0, base=2):
        if isinstance(num_digits, Bin):
            self._num_digits = num_digits._num_digits
            self._val = num_digits._val
        else:
            self._num_digits = int(num_digits)

            if isinstance(val, str):
                self._val = int(val, base)
            else:
                self._val = int(val)

            if num_digits < 1:
                raise ValueError('number of digits must be >= 1')

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
            return Bin(x, self._num_digits)
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
