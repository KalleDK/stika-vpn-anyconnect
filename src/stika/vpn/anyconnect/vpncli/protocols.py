from typing_extensions import Protocol
from typing import IO, Tuple


class Process(Protocol):
    stdin: IO
    stdout: IO

    # noinspection PyShadowingBuiltins
    def communicate(self, input: bytes=None, timeout: int=None) -> Tuple[bytes, bytes]: ...

    def terminate(self) -> None: ...
