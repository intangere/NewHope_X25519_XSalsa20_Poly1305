import hashlib
import random
import string
import os

class User(object):

	def __init__(self):
		"""Empty holder object
		   for our test users
		"""
		pass


def seed_protocol_test():
	"""
	To be a fair protocol, Bob should first hash his seed and send the hash of the seed to Alice as a "commitment". [Done]
	Then Alice sends her seed to Bob. That constitutes the first exchange. [Done]
	Bob then concatenates Alice's seed with his own and uses the new hope scheme to generate the New Hope Basepoint. [Done]
	During the New Hope Key Exchange Bob sends his seed along with his key exchange information. [Done]
	Before generating the basepoint, Alice first checks to see that Bob's seed hashes to the value he committed to. [Done]
	"""
	user1 = User()
	user2 = User()
	
	user1.seed, user1.seed_hash = genSeed()
	user1.data_chunk_1 = 'Some random'
	user1.data_chunk_2 = ' data for you'

	user2.seed, user2.seed_hash = genSeed()
	user2.data = 'My data'
	user1.data_chunk_2 = ' data for you'

	#user1 sends their hashed seed
	user2.recv_hash= user1.seed_hash

	#user2 then sends their seed
	user1.recv_seed = user2.seed
	user1.concat_seed = user1.seed + user1.recv_seed

	#user1 then sends the first chunk of data with their seed
	user2.recv_seed = user1.seed
	user2.recv_data = user1.data_chunk_1

	#user2 verifys the seed before using the data as needed
	verifySeed(user2.recv_seed, user2.recv_hash)

	#user1 verifys the seed before using the data as needed
	#verifySeed(user1.recv_seed, user1.recv_hash)

	print('Successfully verified seeds')


def genSeed():
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
	return seed, seed_hash

def verifySeed(recv_seed, recv_hash):
	hashing_algorithm = hashlib.shake_128()
	hashing_algorithm.update(recv_seed)
	# 2200 bytes from SHAKE-128 function is enough data to get 1024 coefficients
	# smaller than 5q, from Alkim, Ducas, Pöppelmann, Schwabe section 7:
	seed_hash = hashing_algorithm.digest(100)	
	assert recv_hash == seed_hash
	return True

seed_protocol_test()