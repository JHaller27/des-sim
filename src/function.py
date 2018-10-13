# Author: James Haller
from encrypter import Encrypter, R


class Function:
    """
    GoF Context class
    """
    __slots__ = ['_encrypter', '_step', '_data']

    def __init__(self, encrypter: Encrypter):
        self._encrypter = encrypter
        self._step = None
        self._data = None

    def get_result(self):
        self._step = Initialize(self)

        while self._step is not None:
            self._step = self._step.run()

        return self._data


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
        self._context._data = self._context._encrypter.plaintext[R]  # Violates Law of Demeter, but eh
        return Expansion(self._context)


class Expansion(FunctionStep):
    def run(self):
        return None


class Xor(FunctionStep):
    def run(self):
        return None


class SBoxes(FunctionStep):
    def run(self):
        return None


class Permutation(FunctionStep):
    def run(self):
        return None
