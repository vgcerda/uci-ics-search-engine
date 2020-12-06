import hashlib
from collections import defaultdict


def Simhash(words, bits=128):
	# Words is a word : frequency dictionary:
	final_bits = [0 for i in range(bits)]
	for word, frequency in words.items():
		encoded_word = word.encode('utf-8')
		word_hash = int(hashlib.md5(encoded_word).hexdigest(), 16)
		for i in range(bits):
			mask = 1 << i
			if word_hash & mask:
				final_bits[i] += words[word]
			else:
				final_bits[i] -= words[word]

	fingerprint = 0
	for i in range(bits):
		if final_bits[i] >= 0:
			fingerprint += 1 << i

	return fingerprint

# class SimhashDict():
# 	def __init__(self, bits):
# 		self.bits = bits
# 		self.near_duplicates = defaultdict(set())

# 	def add(self, simhash):

	# def has_near_dups(self):


# def Distance(simhash1, simhash2, bits=128):
# 	x = (simhash1 ^ simhash2) & ((1 << bits) - 1)
# 	ret = 0
# 	while x:
# 		ret += 1
# 		x &= x - 1
# 	return ret




