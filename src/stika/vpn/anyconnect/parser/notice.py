import re
from typing import List, Type, Match, Tuple, Optional
from stika.vpn.anyconnect import event
from stika.vpn.anyconnect.event import Event
from .base import StaticSubParser, SubParser, RegexSubParser


class ParseRegistered(StaticSubParser):
    prefix = b'  >> registered with local VPN subsystem.'
    event = event.Registered


class ParseStillActive(StaticSubParser):
    prefix = b'  >> note: VPN Connection is still active.'
    event = event.StillActive


class ParseGoodbye(StaticSubParser):
    prefix = b'goodbye...'
    event = event.Goodbye


class ParseReadyToConnect(StaticSubParser):
    prefix = b'  >> notice: Ready to connect.'
    event = event.ReadyToConnect


class ParseConnectedTo(RegexSubParser):
    prefix = b'  >> notice: Connected to '
    regex = re.compile(b' {2}>> notice: Connected to ([^\r]+).\r')

    @classmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[Event]]:
        return m.endpos, event.ConnectedTo(str(m.group(1), 'utf8'))


class ParseContacting(RegexSubParser):
    prefix = b'  >> notice: Contacting '
    regex = re.compile(b' {2}>> notice: Contacting ([^\r]+).\r')

    @classmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[Event]]:
        return m.endpos, event.Contacting(str(m.group(1), 'utf8'))


class ParseContactingHostForLogin(RegexSubParser):
    prefix = b'  >> contacting host ('
    regex = re.compile(b' {2}>> contacting host \(([^)]+)\) for login information...\r')

    @classmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[Event]]:
        return m.endpos, event.ContactingHostForLogin(str(m.group(1), 'utf8'))


class ParseEstablishingVPN(RegexSubParser):
    prefix = b'  >> notice: Establishing VPN'
    regex = re.compile(b' {2}>> notice: Establishing VPN([^\r]+)\r')

    @classmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[Event]]:
        return m.endpos, event.EstablishingVPN(str(m.group(1), 'utf8'))


PARSERS: List[Type[SubParser]] = [
    ParseRegistered, ParseStillActive, ParseGoodbye, ParseReadyToConnect, ParseContactingHostForLogin, ParseContacting,
    ParseEstablishingVPN, ParseConnectedTo
]
