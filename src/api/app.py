from flask import Flask, jsonify, request, render_template

from src.core.transaction import Transaction

app = Flask(__name__, template_folder='../../templates')
node_instance = None  # Sera rempli au démarrage


@app.route('/mempool', methods=['GET'])
def get_mempool():
    # Accès à la mempool de la blockchain via le nœud
    return jsonify({"mempool": list(node_instance.blockchain.mempool)})

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = 0
    # Accès à la blockchain
    for block in node_instance.blockchain.chain:
        for tx in block.get('transactions', []):
            if tx['sender'] == address: balance -= tx['amount']
            if tx['receiver'] == address: balance += tx['amount']
    return jsonify({"address": address, "balance": balance})


@app.route('/send', methods=['POST'])
def send_transaction():
    data = request.get_json()

    if not all(k in data for k in ('sender', 'receiver', 'amount', 'signature')):
        return jsonify({"status": "error", "message": "Données incomplètes"}), 400

    tx = Transaction(
        data['sender'],
        data['receiver'],
        data['amount'],
        data['signature']
    )

    if node_instance.blockchain.add_transaction(tx):
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Transaction invalide"}), 400

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({
        "length": len(node_instance.blockchain.chain),
        "chain": node_instance.blockchain.chain
    })

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/mine', methods=['GET'])
def mine():
    block = node_instance.blockchain.mine()

    if block:
        node_instance.broadcast("NEW_BLOCK", block)
        return jsonify({"message": "Bloc miné", "block": block})

    return jsonify({"message": "Mempool vide"}), 400

def run_api(node):
    global node_instance
    node_instance = node
    app.run(host='0.0.0.0', port=8080)