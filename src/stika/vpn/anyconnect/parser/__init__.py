import logging
from typing import List, Type
from stika.vpn.anyconnect import event
from .protocols import Receiver
from . import base
from . import misc
from . import state
from . import notice
from . import action
from . import error


logger = logging.getLogger(__name__)


class Parser:

    receivers: List[Receiver]
    buffer: bytes
    parsers: List[Type[base.SubParser]]
    logger: logging.Logger = logger.getChild('Parser')

    def __init__(self):
        self.receivers = list()
        self.buffer: bytes = b''
        self.parsers = [
            *misc.PARSERS,
            *state.PARSERS,
            *notice.PARSERS,
            *action.PARSERS,
            *error.PARSERS,
            base.ParseUnknown,
        ]

    def register(self, receiver: Receiver):
        self.receivers.append(receiver)

    def unregister(self, receiver: Receiver):
        self.receivers.remove(receiver)

    def send(self, ev: event.Event):
        for r in self.receivers:
            r.receive(ev)

    def parse(self) -> bool:
        for sub_parser in self.parsers:
            if self.buffer.startswith(sub_parser.prefix):
                n, ev = sub_parser.parse(self.buffer)

                if n == 0:
                    return False

                self.logger.debug(self.buffer[:n])
                self.buffer = self.buffer[n:]

                if ev is not None:
                    self.send(ev)

                return True

        return False

    def push(self, ch: bytes):

        self.buffer += ch
        while self.parse():
            pass
