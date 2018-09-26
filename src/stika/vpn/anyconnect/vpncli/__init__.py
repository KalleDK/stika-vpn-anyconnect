import os
import pathlib
import subprocess
import logging
import contextlib

from typing import ContextManager

from stika.vpn.anyconnect import event
from stika.vpn.anyconnect.parser import Parser, Receiver

from .protocols import Process
from .processcontainer import ProcessContainer

logger = logging.getLogger(__name__)


DEFAULT_PROGRAM = pathlib.Path(
        os.environ['PROGRAMFILES(X86)'],
        'Cisco',
        'Cisco AnyConnect Secure Mobility Client',
        'vpncli.exe'
    )


class VPNCliContext:
    logger: logging.Logger = logger.getChild('VPNCliContext')
    process: ProcessContainer
    parser: Parser

    def __init__(self, process: ProcessContainer, parser: Parser):
        self.process = process
        self.parser = parser

    @property
    def _stdin(self):
        return self.process.stdin

    @property
    def _stdout(self):
        return self.process.stdout

    def register(self, receiver: Receiver):
        self.parser.register(receiver)

    def unregister(self, receiver: Receiver):
        self.parser.unregister(receiver)

    def _send(self, data: bytes):
        self.logger.debug("sending: {}".format(data + b'\n'))
        self._stdin.write(data + b'\n')
        self._stdin.flush()

    def quit(self):
        self._send(b'quit')

    def disconnect(self):
        self._send(b'disconnect')

    def connect(self, host: str):
        self._send(b'connect ' + bytes(host, 'utf8'))

    def state(self):
        self._send(b'state')

    def stats(self):
        self._send(b'stats')

    def run(self):
        while not self._stdout.closed:
            ch = self._stdout.read(1)
            if ch == b'':
                break
            self.parser.push(ch)


class VPNCliBase:
    logger: logging.Logger = logger.getChild('VPNCliBase')
    program: pathlib.Path
    workdir: pathlib.Path

    def __init__(self, program: os.PathLike = None, workdir: os.PathLike = None):
        self.program = pathlib.Path(program or DEFAULT_PROGRAM)
        self.workdir = pathlib.Path(workdir or self.program.parent)

    def _open(self, args):
        return subprocess.Popen(
            args=[str(self.program), *args],
            cwd=str(self.workdir),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def open_stdin(self):
        return self._open(['-s'])

    def run_disconnect(self):
        return self._open(['disconnect']).communicate()

    def run_state(self):
        return self._open(['state']).communicate()


class VPNCli(VPNCliBase):
    logger: logging.Logger = logger.getChild('VPNCli')
    parser: Parser

    def __init__(self, program: os.PathLike = None, workdir: os.PathLike = None, parser: Parser = None):
        self.parser = parser or Parser()
        VPNCliBase.__init__(self, program, workdir)

    @contextlib.contextmanager
    def open(self) -> ContextManager[VPNCliContext]:
        pc = ProcessContainer(self.open_stdin())
        v = VPNCliContext(pc, self.parser)
        with FixUnknownState(self, pc).patch(v) as v:
            yield v
        pc.communicate(timeout=1)


# This is a fix due to 'vpncli.exe -s' cannot
# get input from stdin if state is Unknown
# this is a bug in the vpncli.exe software
class FixUnknownState:
    def __init__(self, cli: VPNCliBase, pc: ProcessContainer):
        self.cli: VPNCliBase = cli
        self.pc: ProcessContainer = pc

    @contextlib.contextmanager
    def patch(self, v: VPNCliContext):
        v.register(self)
        yield v
        v.unregister(self)

    def receive(self, ev: event.Event):
        if isinstance(ev, event.UnknownState):
            # Terminate soon to be stale process
            self.pc.terminate()

            # Run disconnect command to fix unknown state
            self.cli.run_disconnect()

            # Open a new process and replace the stale/closed
            self.pc.replace(self.cli.open_stdin())
