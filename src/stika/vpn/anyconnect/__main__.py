import logging
from stika.vpn.anyconnect import VPNCli, VPNCliContext
from stika.vpn.anyconnect import event


logger = logging.getLogger(__name__)


class Receiver:

    def __init__(self, vpncli: VPNCliContext):
        self.vpncli = vpncli
        self.booted = False

    def receive(self, ev: event.Event):
        logger.debug("event: {}".format(ev))
        if isinstance(ev, event.State):
            print(ev)
        if isinstance(ev, event.Registered):
            self.booted = True
        if isinstance(ev, event.Prompt) and self.booted:
            print("quitting")
            self.booted = False
            self.vpncli.quit()


def main():
    logging.basicConfig(level=logging.DEBUG)
    vpncli = VPNCli()
    with vpncli.open() as cli:
        cli.register(Receiver(cli))
        cli.run()


if __name__ == "__main__":
    main()
