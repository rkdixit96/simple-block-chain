import os
import requests
import json

from flask import Flask, jsonify, request
from uuid import uuid4

from motuchain import MotuCoin


node_address = str(uuid4()).replace('-', '')

blockchain = MotuCoin()
app = Flask(__name__)


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(
        sender=node_address, receiver=os.getenv('NODE_USER'), amount=1
    )
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Congrats! You mined a block',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions']
    }
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    response = {
        'validity': blockchain.is_chain_valid(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(
        json['sender'], json['receiver'], json['amount']
    )
    response = {
        'message': f'This transaction will be added in block {index}'
    }
    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json['nodes']
    if nodes is None:
        return "No nodes", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': 'All nodes are connected',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    response = {
        'chain_replaced': blockchain.replace_chain(),
        'current_chain': blockchain.chain
    }
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
