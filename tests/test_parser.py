import unittest
from typing import Optional
from stika.vpn.anyconnect import event
from stika.vpn.anyconnect.parser import base, misc
from dataclasses import dataclass


@dataclass
class Entry:
    data: bytes
    should_parse: bool
    size: int
    event: Optional[event.Event]


class ParserBase(unittest.TestCase):

    def run_parser(self, uut, entries):
        for entry in entries:
            with self.subTest(entry=entry):
                entry: Entry = entry
                if not entry.data.startswith(uut.prefix):
                    self.assertFalse(entry.should_parse)
                else:
                    self.assertTrue(entry.should_parse)
                    n, ev = uut.parse(entry.data)
                    self.assertEqual(n, entry.size, "wrong size")
                    self.assertEqual(ev, entry.event, "wrong event")


class TestBaseParsers(ParserBase):
    def test_unknown_parser(self):
        entries = [
            Entry(b'', True, 0, None),
            Entry(b'tre\ndsa', True, 0, None),
            Entry(b'tre\r123\r', True, 4, event.UnknownEvent(b'tre')),
            Entry(b'\r', True, 1, event.UnknownEvent(b'')),
            Entry(b'abc\r', True, 4, event.UnknownEvent(b'abc')),
            Entry(b'\nfds\r', True, 5, event.UnknownEvent(b'\nfds')),
            Entry(b'tre\r123\r', True, 4, event.UnknownEvent(b'tre')),
        ]

        uut = base.ParseUnknown

        self.run_parser(uut, entries)


class TestMiscParsers(ParserBase):
    def test_copyright_parser(self):
        entries = [
            Entry(b'',
                  False,
                  0,
                  None),
            Entry(
                b'Copyright (c) 2004 - 2018 Cisco Systems, Inc.  All Rights Reserved.\r',
                True,
                len(b'Copyright (c) 2004 - 2018 Cisco Systems, Inc.  All Rights Reserved.\r'),
                event.Copyright(b' (c) 2004 - 2018 Cisco Systems, Inc.  All Rights Reserved.')
            )
        ]

        uut = misc.ParseCopyright

        self.run_parser(uut, entries)

    def test_prompt_parser(self):
        entries = [
            Entry(b'', False, 0, None),
            Entry(b'\rVPN> ', False, 0, None),
            Entry(b'VPN>', False, 0, None),
            Entry(b'VPN> ', True, 5, event.Prompt()),
            Entry(b'VPN> \r', True, 5, event.Prompt()),
        ]

        uut = misc.ParsePrompt

        self.run_parser(uut, entries)

