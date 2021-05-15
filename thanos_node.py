from thanos import ThanosChain
from flask import Flask, request, jsonify
import json
import requests
import sys
import uuid 

node_id = uuid.uuid4()
node_id = str(node_id)
port_number = sys.argv[1]
thanos_chain = ThanosChain()
thanos_chain.create_genesis_block()

node_info = {"node_id": node_id, "address": "http://localhost:" + port_number}
nodes = []
nodes.append(node_info)
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

@app.route("/nodes")
def get_nodes():
    return {"nodes" : nodes}

@app.route("/nodes/single")
def get_node():
    return node_info

@app.route("/nodes/append", methods=["POST"])
def append_new_node():
    node_to_append = request.json
    print(node_to_append)
    print(type(node_to_append))
    nodes.append(node_to_append)

    return {"added": node_to_append}

@app.route("/nodes/append/request", methods=["POST"])
def append_request():
    headers = {'Content-type' : "application/json"}
    data = json.dumps(node_info)
    res = requests.post('http://localhost:8000/nodes/append', data=data, headers=headers)
    print(res)
    return {"status" : "success"}

if __name__ == "__main__":
    port_number = int(port_number)
    app.run(debug=True, port=port_number)