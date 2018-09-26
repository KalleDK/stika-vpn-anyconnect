from typing import Any


class Event:
    def __eq__(self, other):
        return isinstance(other, self.__class__)


class UnknownEvent(Event):

    _data: Any

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._data == other._data

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return "Unknown Event: {}".format(self._data)

    def __repr__(self):
        return 'UnknownEvent({})'.format(repr(self._data))
