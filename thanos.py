import hashlib

class Block:
    def __init__(self, nonce, hash, previous_hash, trx):
        self.nonce = nonce 
        self.hash = hash 
        self.trx = trx 
        self.previous_hash = previous_hash
    
    def retrieve_information(self):
        block_info = {
            'previous_hash':self.previous_hash,
            'hash': self.hash,
            'nonce': self.nonce,
            'trx': self.trx
        }