from typing import Tuple, IO
from .protocols import Process


class ProcessContainer:

    _p: Process

    def __init__(self, p: Process):
        self._p = p

    @property
    def stdin(self) -> IO:
        return self._p.stdin

    @property
    def stdout(self) -> IO:
        return self._p.stdout

    # noinspection PyShadowingBuiltins
    def communicate(self, input: bytes = None, timeout: int = None) -> Tuple[bytes, bytes]:
        return self._p.communicate(input=input, timeout=timeout)

    def terminate(self):
        return self._p.terminate()

    def replace(self, p: Process):
        self._p = p
