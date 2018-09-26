from .base import Event


class ActionNeeded(Event):
    pass


class ConnectAnyway(ActionNeeded):
    def __init__(self, hostname: str):
        self.hostname = hostname

    def __str__(self):
        return "connect anyway to: {}".format(self.hostname)


class AlwaysTrustServer(ActionNeeded):
    def __str__(self):
        return "always trust this server"


class UsernameRequest(ActionNeeded):
    def __str__(self):
        return "username"


class PasswordRequest(ActionNeeded):
    def __str__(self):
        return "password"
