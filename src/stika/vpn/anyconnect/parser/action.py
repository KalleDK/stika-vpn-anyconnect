import re
from typing import Match, Tuple, Optional, List, Type
from stika.vpn.anyconnect import event
from stika.vpn.anyconnect.event import Event
from .base import StaticSubParser, RegexSubParser, SubParser


class ParseAlwaysTrustServer(StaticSubParser):
    prefix = b'Always trust this server and import the certificate? [y/n]: '
    event = event.AlwaysTrustServer


class ParseConnectAnyway(RegexSubParser):
    prefix = b'AnyConnect cannot verify server: '
    regex = re.compile(b'AnyConnect cannot verify server: ([^\r]+)\r.*Connect Anyway\? \[y/n\]: ', re.DOTALL)

    @classmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[Event]]:
        return m.end(0), event.ConnectAnyway(str(m.group(1), 'utf8'))


class ParseUsernameRequest(StaticSubParser):
    prefix = b'Username: '
    event = event.UsernameRequest


class ParsePasswordRequest(StaticSubParser):
    prefix = b'Password: '
    event = event.PasswordRequest


PARSERS: List[Type[SubParser]] = [
    ParseConnectAnyway, ParseAlwaysTrustServer, ParseUsernameRequest, ParsePasswordRequest
]
