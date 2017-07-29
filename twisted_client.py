#!/usr/bin/env python
"""UDP hole punching client."""
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import random
import string
import time
import json
from nhxpoly.nhxpoly import NewHopeXSPolyBox
from newhope import newhope
import random
import string
import sys
import pickle

# a client protocol

box = NewHopeXSPolyBox()
box.name = sys.argv[1]
box.init = False

class ClientProtocol(DatagramProtocol):
    """
    Client protocol implementation.
    The clients registers with the rendezvous server.
    The rendezvous server returns connection details for the other peer.
    The client Initializes a connection with the other peer and sends a
    message.
    """

    def startProtocol(self):
        """Register with the rendezvous server."""
        self.server_connect = False
        self.peer_init = False
        self.peer_connect = False
        self.peer_address = None
        self.transport.write('0'.encode(), ('0.0.0.0', 7654))

    def toAddress(self, data):
        #data = data#.decode()
        """Return an IPv4 address tuple."""
        data = data.decode()
        ip, port = data.split(':')
        return (ip, int(port))

    def checkFormat(self, datagram):
        if '.' in datagram and ':' in datagram:
            if len(datagram.split('.')) == 4 and len(datagram.split(':')) == 2:
                return True
        return False

    def datagramReceived(self, datagram, host):
        #print('Incoming data: ' + repr(datagram))
        """Handle incoming datagram messages."""
        """
        if not self.server_connect:
            self.server_connect = True
            self.transport.write('ok'.encode(), (rendevous_ip, rendevous_port))
            print('Connected to server, waiting for peer...')
        """
        if datagram == b'0':
            return

        if datagram == b'ok' and not self.server_connect:
            print('Successfully connected to rendezvous server')
            self.server_connect = True

        elif not self.peer_init:
            self.peer_address = self.toAddress(datagram)
            self.peer_init = True
            self.transport.write('init'.encode(), self.peer_address)
            print('Sent init to %s:%d' % self.peer_address)

        elif not self.peer_connect:
            self.peer_connect = True
            host = self.transport.getHost().host
            port = self.transport.getHost().port
            self.transport.write('0'.encode(), self.peer_address)
            if box.name == 's':
                self.transport.write(box.initCode(), self.peer_address)
                print('Sent NewHope_X25519_XSalsa20_Poly1305 init')
                box.genPrekeyChunk()
                box._state = 2

        else:
            print(box._state)
            if datagram == box.initCode():
                box.createSealedBox()
                print('Peer to peer NewHope_X25519_XSalsa20_Poly1305 key exchange started')
                self.transport.write(box.pk, self.peer_address)
                print('Sent X25519_XSalsa20_Poly1305 Sealed Box Key %s' % repr(box.pk))
                box._state = 3

            elif box._state == 2:
                box.setSenderPubKey(datagram)
                print('Recieved X25519_XSalsa20_Poly1305 Sealed Box Key %s' % repr(box.sender_nacl_pubkey))
                box.encryptPrekeyChunk()
                self.transport.write(box.enc_prekey_chunk_1, self.peer_address)
                print('Prekey chunk 1: %s' % box.prekey_chunk_1)
                print('Sent encrypted prekey chunk 1')
                box.genSeed()
                box._state = 4

            elif box._state == 3:
                box.enc_prekey_chunk_1 = datagram
                box.openSealedBox()
                print('Opened sealed box containing prekey chunk 1 %s' % box.prekey_chunk_1)
                box.genSeed()
                self.transport.write(box.seed_hash, self.peer_address)
                print('Sent shake_128 hashed HewHope commitment seed: %s' % box.seed_hash)
                box._state = 5

            elif box._state == 4:
                box.recv_hash = datagram
                self.transport.write(box.seed, self.peer_address)
                print('Recieved NewHope commitment hash: %s' % box.recv_hash)
                print('Sent NewHope raw commitment seed: %s' % box.seed)
                shaked = False
                while not shaked:
                    try:
                        box.initNewHope()
                        shaked = True
                    except Exception as e:
                        pass
                box._state = 6
               

            elif box._state == 5:
                box.recv_seed = datagram
                print('Recieved NewHope seed hash: %s' % box.recv_seed)
                self.transport.write(box.seed, self.peer_address)
                print('Sent clear NewHope seed')
                shaked = False
                while not shaked:
                    try:
                        box.initNewHope()
                        shaked = True
                    except Exception as e:
                        pass
                self.transport.write(pickle.dumps(box.message), self.peer_address)
                print('Sent NewHope initial message %s' % repr(box.message))
                box._state = 7

            elif box._state == 6:
                box.recv_seed = datagram
                box.verifySeed()
                print('Seeds verified')
                box._state = 8
                #send the second new hope message

            elif box._state == 7:
                box.recv_message = pickle.loads(datagram)
                print('Recieved NewHope message: %s' % repr(box.recv_message))
                box.message = newhope.shareda(box.recv_message)
                #self.transport.write(pickle.dumps(box.message), self.peer_address)
                box.createNewHopeSharedKeya()
                print('Shared key: %s' % box.shared_newhope_key)
                box._state = 9

            elif box._state == 8:
                box.recv_message = pickle.loads(datagram)
                print('Received NewHope message: %s' % repr(box.recv_message))
                box.message = newhope.sharedb(box.recv_message)
                self.transport.write(pickle.dumps(box.message), self.peer_address)
                box.createNewHopeSharedKeyb()
                print('Shared key: %s' % box.shared_newhope_key)
                box._state = 9


    def stopProtocol(self):
        print('Stopped')

if __name__ == '__main__':

    protocol = ClientProtocol()
    t = reactor.listenUDP(0, protocol)
    reactor.run()