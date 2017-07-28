#NewHope_X25519_XSalsa20_Poly1305 Implementation by e
from newhope import newhope
import libnacl.utils
import libnacl
import hashlib
import random
import string
import os
import sys


class NewHopeXSPolyBox():

	def __init__(self):
		self._state = 0

	def setState(self):
		self._state += state

	def clearState(self):
		self._state = 0

	def initCode(self):
		return b'\x0b'

	def genPrekeyChunk(self, size = 32):
		self.prekey_chunk_1 = os.urandom(size)

	def log(self, msg):
		print('[%s]: %s' % (self.name, msg))

	def createSealedBox(self):
		self.pk, self.sk = libnacl.crypto_box_keypair()

	def setSenderPubKey(self, pk):
		self.sender_nacl_pubkey = pk

	def encryptPrekeyChunk(self):
		self.enc_prekey_chunk_1 = libnacl.crypto_box_seal(self.prekey_chunk_1, self.sender_nacl_pubkey)
		assert self.enc_prekey_chunk_1 != self.prekey_chunk_1

	def openSealedBox(self):
		self.prekey_chunk_1 = libnacl.crypto_box_seal_open(self.enc_prekey_chunk_1, self.pk, self.sk)

	def initNewHope(self):
		self.message = newhope.keygen(True)

	def createNewHopeSharedKey(self):
		self.shared_newhope_key = newhope.b_key

	def combine_prekey_chunks(self):
		combined = []
		for x in self.shared_newhope_key:
			combined.append(x)
		for x in self.prekey_chunk_1:
			combined.append(x)
		self.prekey = combined

	def genSeed(self):
		"""Generates a cryptographically secure random string of numbers
		   which for our purposes acts as a private seed.
		   Then we use shake_128 to generate a secure hash of the seed
		   Both are returned
		"""
		seed_length = int(''.join(random.SystemRandom().choice(string.digits) for _ in range(0, 3)))
		seed = os.urandom(seed_length)
		hashing_algorithm = hashlib.shake_128()
		hashing_algorithm.update(seed)
		# 2200 bytes from SHAKE-128 function is enough data to get 1024 coefficients
		# smaller than 5q, from Alkim, Ducas, Pöppelmann, Schwabe section 7:
		seed_hash = hashing_algorithm.digest(100)
		self.seed = seed
		self.seed_hash = seed_hash

	def verifySeed(self):
		hashing_algorithm = hashlib.shake_128()
		hashing_algorithm.update(self.recv_seed)
		# 2200 bytes from SHAKE-128 function is enough data to get 1024 coefficients
		# smaller than 5q, from Alkim, Ducas, Pöppelmann, Schwabe section 7:
		seed_hash = hashing_algorithm.digest(100)	
		assert seed_hash == self.recv_hash
		return True
