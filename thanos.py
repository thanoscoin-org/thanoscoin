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

class ThanosChain:
    def __init__(self):
        self.temp_trx = []

    def create_block():
        pass 

    def create_transaction():
        pass

    def proof_of_work():
        pass

    def create_block_data():
        pass