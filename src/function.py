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

    def run(self):
        self._data = self._encrypter.plaintext(R)
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


class Initialize(FunctionStep):
    def run(self):
        return None
