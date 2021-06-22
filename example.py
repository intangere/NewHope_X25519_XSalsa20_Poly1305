from nhxpoly.nhxpoly import NewHopeXSPolyBox
from newhope import newhope
from hashlib import sha256

"""This file shows a test run of
   the NewHope_X25519_XSalsa20_Poly1305
   key exchange protocol"""

user1 = NewHopeXSPolyBox()
user1.name = 'Alice'
user1.genPrekeyChunk()
user1.log('Prekey chunk created: %s' % repr([x for x in user1.prekey_chunk_1]))

user2 = NewHopeXSPolyBox()
user2.name = 'Bob'
user2.createSealedBox()

user1.setSenderPubKey(user2.pk)
user2.log('Created a X25519_XSalsa20_Poly1305 sealed box and sent public key to %s' % user1.name)

user1.encryptPrekeyChunk()
user1.log('Encrypted prekey chunk using the recieved X25519 Public Key via unidentifiable authentication.')

user2.enc_prekey_chunk_1 = user1.enc_prekey_chunk_1
user2.openSealedBox()
user2.log('First prekey chunk decrypted %s' % repr([x for x in user2.prekey_chunk_1]))

user1.genSeed()
user2.genSeed()

user1.initNewHope()
user1.genCommitmentHash()

user2.recv_commitment = user1.commitment #user1 sends commitment hash
user2.log('NewHope Seed commitment received with hash %s' % user2.recv_commitment)

user2.recv_message = user1.message
user2.recv_seed = user1.seed #user1 sends (reveals) seed

user2.verifyCommitment()
user2.log('Seed verification succeded. Authentic NewHope message recieved')

user2.message = newhope.sharedb(user1.message)
user1.log('NewHope initial authenticated message exchanged')

user2.genCommitmentHash()

user1.recv_commitment = user2.commitment #User2 sends commitment
user1.log('NewHope Seed commitment received with hash %s' % user1.recv_commitment)

user1.recv_message = user2.message
user1.recv_seed = user2.seed

user1.verifyCommitment()
user1.log('Seed verification succeded. Authentic NewHope message recieved')

user1.message = newhope.shareda(user2.message)
user1.log('NewHope final authenticated message exchanged')

user2.createNewHopeSharedKeyb()
user1.createNewHopeSharedKeya()

assert user2.shared_newhope_key == user1.shared_newhope_key

user2.log('NewHope shared key %s' % user2.shared_newhope_key)
user1.log('NewHope shared key %s' % user1.shared_newhope_key)

user2.combine_prekey_chunks()
user1.combine_prekey_chunks()

user2.log('Combined prekey %s' % user2.prekey)
user1.log('Combined prekey %s' % user1.prekey)

print('NewHope_X25519_XSalsa20_Poly1305 key exchange successful.')
print('Pre-key ready for key derivation..')

#Very simple possible key-derivation...
def derive(prekey):
  prekey = ''.join([chr(_) for _ in prekey])
  prekey = prekey.encode()
  return sha256(prekey).hexdigest()

user1.log('Derived key:' + derive(user1.prekey))
user2.log('Derived key:' + derive(user2.prekey))

assert derive(user1.prekey) == derive(user2.prekey)
print('Derived keys match!')
