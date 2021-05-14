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

        return block_info

class ThanosChain:
    def __init__(self):

        self.chain = []
        self.temp_trx = []

    def create_block(self):

        last_block = self.chain[-1]
        previous_hash = last_block['previous_hash']

        nonce, block_hash = self.proof_of_work()

        self.block = Block(nonce=nonce, hash=block_hash, previous_hash=previous_hash, trx=self.temp_trx)
        self.chain.append(self.block.retrieve_information())
        self.temp_trx = []

        return self.block.retrieve_information

    def create_transaction(self, sender, recipient, amount):
        
        transaction_data = sender + ", " + recipient + ", " + str(amount)
        transaction_id = hashlib.md5(transaction_data.encode()).hexdigest()
        transaction = {
            'transaction_id': transaction_id,
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self.temp_trx.append(transaction)

    def proof_of_work(self):
        last_block = self.chain[-1]
        previous_hash = last_block['previous_hash']
        nonce = str(last_block['nonce'])
        hash = last_block['hash']

        input_string = previous_hash + "-" + nonce + "-" + hash

        salt = 0 
        while True:
            input_string = input_string + str(salt)
            temp_hash = hashlib.sha256(input_string.encode()).hexdigest()
            if temp_hash[:4] == 'ffff':
                break
            else:
                salt += 1
        
        return salt, temp_hash

    def create_genesis_block(self):
        nonce = 0 
        previous_hash = "140264396"
        trx = []

        block_data = str(nonce) + previous_hash + str(trx)
        hash = hashlib.sha256(block_data.encode()).hexdigest()

        genesis = Block(nonce=nonce, hash=hash, previous_hash=previous_hash, trx=trx)
        self.chain.append(genesis.retrieve_information())
        