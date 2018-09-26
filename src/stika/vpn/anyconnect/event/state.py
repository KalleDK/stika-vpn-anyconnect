from .base import Event


class State(Event):
    pass


class UnknownState(State):
    def __str__(self):
        return "unknown"


class Disconnecting(State):
    def __str__(self):
        return "disconnecting"


class Disconnected(State):
    def __str__(self):
        return "disconnected"


class Connecting(State):
    def __str__(self):
        return "connecting"


class Connected(State):
    def __str__(self):
        return "connected"


class Reconnecting(State):
    def __str__(self):
        return "reconnecting"

