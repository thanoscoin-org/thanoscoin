from thanos import ThanosChain, MAX_COIN_CAPACITY
from flask import Flask, request, jsonify
import json
import requests
import sys
import uuid 

node_id = uuid.uuid4()
node_id = str(node_id)
port_number = sys.argv[1]
node_info = {"node_id": node_id, "address": "http://localhost:" + port_number}
nodes = []
nodes.append(node_info)
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
    
    if thanos_chain.create_transaction(sender=sender, recipient=recipient, amount=amount):
        return {"message" : "Khaby face..."}
    else:
        return {"message" : "TRX Updted"}
          
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
    global MAX_COIN_CAPACITY 
    MAX_COIN_CAPACITY -= reward_amount
    thanos_chain.create_transaction(sender=node_id, recipient=miner_device, amount=reward_amount)

    thanos_chain.create_block()

    return {"message" : "This is your destiny, my child"}

@app.route("/nodes")
def get_nodes():
    return {"nodes" : set(list(nodes))}

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

@app.route("/nodes/broadcast", methods=["POST"])
def broadcast():
    nodes_from_genesis = request.json 
    print(nodes_from_genesis)
    nodes.extend(nodes_from_genesis)
    return {"status" : "success"}

@app.route("/nodes/sync", methods=["POST"])
def sync_nodes():
    header = {'Content-type' : 'application/json'}
    for node in set(list(nodes)):
        requests.post(node['address'] + "/nodes/broadcast", data=json.dumps(nodes), headers=header)
    
    return {"synchorinzation" : "done"}

@app.route('/coins_available')
def coins_available():
    return {"coins_available" : MAX_COIN_CAPACITY}

if __name__ == "__main__":
    port_number = int(port_number)
    app.run(debug=True, port=port_number)