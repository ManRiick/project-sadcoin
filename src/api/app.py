from flask import Flask, jsonify, request, render_template
from src.core.transaction import Transaction

# Initialize Flask application with the path to the frontend templates
app = Flask(__name__, template_folder='../../templates')
node_instance = None  # Placeholder for the P2P node instance, injected at runtime


@app.route('/mempool', methods=['GET'])
def get_mempool():
    """Retrieve the list of unconfirmed transactions currently in the mempool."""
    # Direct access to the blockchain's mempool via the injected node instance
    return jsonify({"mempool": list(node_instance.blockchain.mempool)})

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """Calculate the balance for a specific address by scanning the entire ledger."""
    balance = 0
    #
    # Iterates through every block and every transaction to compute the net balance
    for block in node_instance.blockchain.chain:
        for tx in block.get('transactions', []):
            if tx['sender'] == address:
                balance -= tx['amount']
            if tx['receiver'] == address:
                balance += tx['amount']
    return jsonify({"address": address, "balance": balance})


@app.route('/send', methods=['POST'])
def send_transaction():
    """Receive and validate a new transaction from the web wallet."""
    data = request.get_json()

    # Ensure all required cryptographic and financial fields are present
    if not all(k in data for k in ('sender', 'receiver', 'amount', 'signature')):
        return jsonify({"status": "error", "message": "Incomplete data"}), 400

    # Instantiate a Transaction object to leverage its internal validation logic
    tx = Transaction(
        data['sender'],
        data['receiver'],
        data['amount'],
        data['signature']
    )

    # Attempt to add the transaction to the local mempool (includes signature check)
    if node_instance.blockchain.add_transaction(tx):
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Invalid transaction"}), 400

@app.route('/chain', methods=['GET'])
def get_chain():
    """Expose the full blockchain ledger as a JSON object for synchronization or inspection."""
    return jsonify({
        "length": len(node_instance.blockchain.chain),
        "chain": node_instance.blockchain.chain
    })

@app.route('/')
def index():
    """Serve the primary dashboard/wallet interface."""
    return render_template("index.html")

@app.route('/mine', methods=['GET'])
def mine():
    """Trigger the Proof of Work process for the current mempool and broadcast the result."""
    # Attempt to mine a new block based on pending transactions
    block = node_instance.blockchain.mine()

    if block:
        #
        # Propagate the successfully mined block to all connected peers in the P2P network
        node_instance.broadcast("NEW_BLOCK", block)
        return jsonify({"message": "Block mined successfully", "block": block})

    # Return error if there are no transactions to mine
    return jsonify({"message": "Mempool is empty"}), 400

def run_api(node):
    """Entry point to start the Flask server with dependency injection of the P2P node."""
    global node_instance
    node_instance = node
    # Listen on all network interfaces (required for Docker networking) on port 8080
    app.run(host='0.0.0.0', port=8080)