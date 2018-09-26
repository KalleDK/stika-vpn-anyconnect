from .base import Event


class Notice(Event):
    pass


class ReadyToConnect(Notice):
    def __str__(self):
        return "ready to connect"


class Contacting(Notice):

    host: str

    def __init__(self, host: str):
        self.host = host

    def __str__(self):
        return "contacting [{}]".format(self.host)


class EstablishingVPN(Notice):

    data: str

    def __init__(self, data: str):
        self.data = data

    def __str__(self):
        return "establishing vpn [{}]".format(self.data)


class ConnectedTo(Notice):

    host: str

    def __init__(self, host: str):
        self.host = host

    def __str__(self):
        return "connected to [{}]".format(self.host)


class Registered(Notice):

    def __str__(self):
        return "registered with local VPN subsystem"


class Goodbye(Notice):

    def __str__(self):
        return "goodbye"


class StillActive(Notice):

    def __str__(self):
        return "vpn is still active"


class ContactingHostForLogin(Notice):
    def __init__(self, hostname: str):
        self.hostname = hostname

    def __str__(self):
        return "contacting {} for login".format(self.hostname)
