from thanos import ThanosChain
from flask import Flask, request
import sys
import uuid 

node_id = uuid.uuid4()
node_id = str(node_id)
thanos_chain = ThanosChain()
thanos_chain.create_genesis_block()

app = Flask(__name__)

@app.route('/')
def index():
    return {"message": "Welcome, my child"}

@app.route('/create_transaction', methods=["POST"])
def create_transaction():
    data = request.json
    sender = data['sender']
    recipient = data['recipient']
    amount = data['amount']
    
    thanos_chain.create_transaction(sender=sender, recipient=recipient, amount=amount)

    return {"message" : "TRX updated"}

@app.route('/transactions')
def get_transactions():
    return {"trx" : thanos_chain.temp_trx}

@app.route('/blockchain')
def get_chain():
    return {"blockcain" : thanos_chain.chain}

@app.route('/mine', methods=["POST"])
def mine():
    data = request.json
    miner_device = data["device_id"]

    reward_amount = 100
    thanos_chain.create_transaction(sender=node_id, recipient=miner_device, amount=reward_amount)

    thanos_chain.create_block()

    return {"message" : "This is your destiny, my child"}

if __name__ == "__main__":
    port_number = sys.argv[1]
    port_number = int(port_number)
    app.run(debug=True, port=port_number)