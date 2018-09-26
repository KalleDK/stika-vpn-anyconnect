import abc
import re
import logging
from typing import Optional, Tuple, Pattern, Match, Type
from stika.vpn.anyconnect.event import Event, UnknownEvent


logger = logging.getLogger(__name__)


class SubParser(metaclass=abc.ABCMeta):

    prefix: bytes = b''

    @classmethod
    @abc.abstractmethod
    def parse(cls, buffer: bytes) -> Tuple[int, Optional[Event]]:
        raise NotImplemented()


class StaticSubParser(SubParser):

    event: Type[Event]
    logger: logging.Logger = logger.getChild('StaticSubParser')

    @classmethod
    def parse(cls, buffer: bytes) -> Tuple[int, Optional[Event]]:
        return len(cls.prefix), cls.event() if cls.event is not None else None


class RegexSubParser(SubParser):

    regex: Pattern[bytes]
    logger: logging.Logger = logger.getChild('StaticSubParser')

    @classmethod
    @abc.abstractmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[Event]]:
        raise NotImplemented

    @classmethod
    def parse(cls, buffer: bytes) -> Tuple[int, Optional[Event]]:
        m = cls.regex.match(buffer)
        if m is None:
            return 0, None
        return cls._parse_regex(m)


class ParseUnknown(RegexSubParser):

    regex = re.compile(b'([^\r]*)\r')

    @classmethod
    def _parse_regex(cls, m: Match[bytes]) -> Tuple[int, Optional[Event]]:
        return m.end(0), UnknownEvent(m.group(0)[:-1])
