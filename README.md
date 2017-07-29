# NewHope_X25519_XSalsa20_Poly1305
Post Quantum key exchange with NewHope and NaCl (requires Python3.6)
<hr>
(For the love of everything holy please do not use this yet. This is the very first version and many things will change.)<br>
<h1>Description</h1><br>
This library aims to combine the post-quantum NewHope encryption and X25519 elliptical curve cryptography.<br>
The key exchange takes place over two seperate encryption algorithms SIMILIAR but different to Google's CECPQ1 protocol using in Chrome Canary.<br>
First a random 32 byte key chunk is created by the software initiating the key exchange.<br>
The sender who wants to create the encrypted channels then creates a X25519_XSalsa20_Poly1305 key pair and sends it the exchange requester.<br>
The exchange requester encrypts the first 32 byte chunk and sends it back to the sender.<br>
This concludes the first half of the key exchange.<br> 
The requester then begins a commitment protocol which is essentially a way to verify that an eavesdropper isn't tampering with the NewHope key exchange.<br>
The sender sends a random shake_128 hashed seed to the requester.<br>
The requester stores this, then sends the requester their own unhashed seed.<br>
The sender then sends their unhashed seed and first sequence of the NewHope Basepoint.<br>
The requester verifies the seed matches the shake_128 hash.<br>
If so a the requester sends their NewHope Basepoint and an authentice NewHope Key exchange has taken place.<br>
Both the sender and requester can now generate their shared secret key.<br>
Both then combine the two shared key chunks to form a prekey.<br>
This key can now be used to start some sort of encrypted channel of the users choice.<br> 
 
Here is output from a test use of the protocol in example.py<br>
```
[Alice]: Prekey chunk created: [246, 249, 178, 233, 90, 176, 68, 123, 40, 78, 164, 188, 88, 201, 83, 215, 37, 12, 167, 91, 81, 84, 150, 71, 134, 13, 0, 28, 155, 106, 229, 184]
[Bob]: Created a X25519_XSalsa20_Poly1305 sealed box and sent public key to Alice
[Alice]: Encrypted prekey chunk using the recieved X25519 Public Key via unidentifiable authentication.
[Bob]: First prekey chunk decrypted [246, 249, 178, 233, 90, 176, 68, 123, 40, 78, 164, 188, 88, 201, 83, 215, 37, 12, 167, 91, 81, 84, 150, 71, 134, 13, 0, 28, 155, 106, 229, 184]
[Bob]: NewHope Seed commitment received with seed hash b'\xa6z\xba\x88\xe7\xb0\xaf\n\xec6\x9e\xbb\x83\x12[6)i\x9f\x18\xdd\nZ^\xbcyG\x96  U\xe6\x1d\x1f\x80\x14\xb5G\x13k:!u.g\xcc\x88\xa1\xdcX\x95\xd0\xdd\xcbO=\xf3\xa4\xe6\x93hC\xca9t\xf5\x7f\xe4\x0f\x1d~\xe7\x93\x11xPU\xbaU\x10\r\x07\x8f\xf8H\xbct\xdb\x0f\xb0\xd0D{xg\x9b\xe4\x8e\xe0\xf5'
[Alice]: NewHope initial message exchange sent
[Bob]: Seed verification succeded. Authentic NewHope message recieved
[Alice]: Recieved final NewHope message
[Bob]: NewHope shared key [191, 178, 30, 43, 31, 35, 94, 65, 96, 174, 186, 240, 173, 159, 110, 133, 27, 123, 113, 147, 112, 95, 241, 108, 210, 57, 145, 199, 3, 36, 242, 81]
[Alice]: NewHope shared key [191, 178, 30, 43, 31, 35, 94, 65, 96, 174, 186, 240, 173, 159, 110, 133, 27, 123, 113, 147, 112, 95, 241, 108, 210, 57, 145, 199, 3, 36, 242, 81]
[Bob]: Combined prekey [191, 178, 30, 43, 31, 35, 94, 65, 96, 174, 186, 240, 173, 159, 110, 133, 27, 123, 113, 147, 112, 95, 241, 108, 210, 57, 145, 199, 3, 36, 242, 81, 246, 249, 178, 233, 90, 176, 68, 123, 40, 78, 164, 188, 88, 201, 83, 215, 37, 12, 167, 91, 81, 84, 150, 71, 134, 13, 0, 28, 155, 106, 229, 184]
[Alice]: Combined prekey [191, 178, 30, 43, 31, 35, 94, 65, 96, 174, 186, 240, 173, 159, 110, 133, 27, 123, 113, 147, 112, 95, 241, 108, 210, 57, 145, 199, 3, 36, 242, 81, 246, 249, 178, 233, 90, 176, 68, 123, 40, 78, 164, 188, 88, 201, 83, 215, 37, 12, 167, 91, 81, 84, 150, 71, 134, 13, 0, 28, 155, 106, 229, 184]
NewHope_X25519_XSalsa20_Poly1305 key exchange successful.
```
<br>
I've added an example implementation that uses your network via Twisted todo the key exchange.<br>
There's a rendezvous server to directly link to clients p2p via UDP hole punching.<br>
So the key exchange takes place with no middle man.<br>
Here's how you can test it: (Run each command in a seperate console/terminal window<br>
```
python3.6 twisted_server.py 
python3.6 twisted_client.py r
python3.6 twisted_client.py s
```
<b>Warning</b>
This is the bare minimum possible implementation in twisted. There is no packet structure and a few bugs<br>
and very poor error handling. This will be updated in the future when I have more time.<br>
I just wanted to demonstrate one way in which you can implement the key exchange over a network.<br>
