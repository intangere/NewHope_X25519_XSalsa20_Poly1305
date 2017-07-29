"""UDP hole punching server."""
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import sys

rendezvous_port = 7654

class ServerProtocol(DatagramProtocol):

    def __init__(self):
        """Initialize with empty address list."""
        self.addresses = []

    def addressString(self, address):
        """Return a string representation of an address."""
        ip, port = address
        return ':'.join([ip, str(port)])

    def datagramReceived(self, datagram, address):
        """Handle incoming datagram messages."""
        print('Got connection')
        datagram = datagram.decode()
        if datagram == '0':
            print('Registration from %s:%d' % address)
            self.transport.write('ok'.encode(), address)
            self.addresses.append(address)

            if len(self.addresses) >= 2:
                msg_0 = self.addressString(self.addresses[1])
                msg_1 = self.addressString(self.addresses[0])

                self.transport.write(msg_0.encode(), self.addresses[0])
                self.transport.write(msg_1.encode(), self.addresses[1])

                self.addresses.pop(0)
                self.addresses.pop(0)

                print('Linked peers')

    def stopProtocol(self):
        print('Peers linked, disconnected both.')

if __name__ == '__main__':

    reactor.listenUDP(rendezvous_port, ServerProtocol())
    print('Listening on *:%d' % (rendezvous_port))
    reactor.run()
