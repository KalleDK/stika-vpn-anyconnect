from typing import List, Type
from .base import StaticSubParser, SubParser
from stika.vpn.anyconnect import event


class ParseUnknownState(StaticSubParser):
    prefix = b'  >> state: Unknown'
    event = event.UnknownState


class ParseDisconnectedState(StaticSubParser):
    prefix = b'  >> state: Disconnected'
    event = event.Disconnected


class ParseConnectedState(StaticSubParser):
    prefix = b'  >> state: Connected'
    event = event.Connected


class ParseConnectingState(StaticSubParser):
    prefix = b'  >> state: Connecting'
    event = event.Connecting


PARSERS: List[Type[SubParser]] = [
    ParseDisconnectedState, ParseConnectedState, ParseConnectingState, ParseUnknownState
]
