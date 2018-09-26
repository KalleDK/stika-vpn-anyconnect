from . import base


class Error(base.Event):
    pass


class ConnectNotAvailable(Error):
    def __str__(self):
        return "connect not available."


class VPNClientStateNotConnected(Error):
    def __str__(self):
        return "vpn client state is not connected"
