from .base import Event


class Prompt(Event):
    def __str__(self):
        return 'prompt'


class Copyright(Event):

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def __str__(self):
        return 'Copyright {}'.format(str(self.data, 'utf8'))


class Cisco(Event):

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def __str__(self):
        return 'Cisco {}'.format(str(self.data, 'utf8'))


class ProvideCredentials(Event):
    def __str__(self):
        return "provide credentials"
