from time import time
import json
import hashlib

class Blockchain:
	def __init__(self):
		self.chain = []
		self.current_transactions = []
		self.new_block(previous_hash=1, proof=100)
	
	def proof_of_work(self, last_proof:int):
		proof = 0
		while self.valid_proof(last_proof, proof, 4) is False:
			proof += 1
		return proof


	@staticmethod
	def valid_proof(last_proof:int, proof:int, dificulty:int):
		guess = (str(last_proof) + str(proof)).encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:dificulty] == '0'*dificulty


	def new_block(self, proof, previous_hash=None):
		block = {
			'index': len(self.chain) + 1,
			'timestamp' : time(),
			'transactions' : self.current_transactions,
			'proof' : proof,
			'previous_hash' : previous_hash or self.hash(self.chain[-1]),
		}
		self.current_transactions = []
		return block

	def new_transaction(self, sender:str, recipient:str, amount:str):
		self.current_transactions.append({
			'sender' : sender,
			'recipient' : recipient,
			'amount' : amount,
		})
		return self.last_block['index'] + 1

	@staticmethod
	def hash(block)->str:
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()
	
	@property
	def last_block(self):
		return self.chain[-1]
