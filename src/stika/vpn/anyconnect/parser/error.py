import re
from typing import Match, Tuple, Optional, List, Type
from stika.vpn.anyconnect import event
from stika.vpn.anyconnect.event import Event
from . import base


class ParseConnectNotAvailable(base.RegexSubParser):
    prefix = b'  >> error: Connect not available. Another AnyConnect application is running'
    regex = re.compile(b' {2}>> error: Connect not available. Another AnyConnect application is running[\r\n]+'
                       b'or this functionality was not requested by this application.\r', re.DOTALL)

    @classmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[Event]]:
        return m.end(0), event.ConnectNotAvailable()


class ParseVPNClientStateNotConnected(base.StaticSubParser):
    prefix = b'  >> The VPN client state is not "Connected".\r'
    event = event.VPNClientStateNotConnected


PARSERS: List[Type[base.SubParser]] = [
    ParseConnectNotAvailable, ParseVPNClientStateNotConnected,
]
