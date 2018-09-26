from typing_extensions import Protocol
from stika.vpn.anyconnect.event import Event


class Receiver(Protocol):
    def receive(self, event: Event): ...
