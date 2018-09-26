import re
from typing import Match, Tuple, Optional, List, Type
from stika.vpn.anyconnect import event
from .base import StaticSubParser, RegexSubParser, SubParser


class ParsePrompt(StaticSubParser):
    prefix = b'VPN> '
    event = event.Prompt


class ParseNewLine(StaticSubParser):
    prefix = b'\n'
    event = None


class ParseCarriageReturn(StaticSubParser):
    prefix = b'\r'
    event = None


class ParseCisco(RegexSubParser):
    prefix = b'Cisco'
    regex = re.compile(b'Cisco ([^\r]*)\r')

    @classmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[event.Event]]:
        return m.end(0), event.Cisco(m.group(1))


class ParseCopyright(RegexSubParser):
    prefix = b'Copyright'
    regex = re.compile(b'Copyright ([^\r]*)\r')

    @classmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[event.Event]]:
        return m.end(0), event.Copyright(m.group(1))


class ParseCredentials(StaticSubParser):
    prefix = b'  >> Please provide your credentials'
    event = event.ProvideCredentials


PARSERS: List[Type[SubParser]] = [
    ParsePrompt, ParseNewLine, ParseCarriageReturn, ParseCisco, ParseCopyright, ParseCredentials
]
