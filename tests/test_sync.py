from src.core.blockchain import Blockchain
from src.core.transaction import Transaction
from src.crypto.wallet import Wallet


def test_blockchain_sync():
    node1_blockchain = Blockchain()
    node2_blockchain = Blockchain()
    wallet = Wallet()

    # --- CORRECTION ICI ---
    sender_pub = wallet._public_key.to_string().hex()
    receiver = "addr_dest"
    amount = 10
    # On crée le message exact qui sera signé
    data = f"{sender_pub}{receiver}{amount}"
    signature = wallet.sign_transaction(data)

    tx = Transaction(sender_pub, receiver, amount, signature)
    # ----------------------

    node1_blockchain.add_transaction(tx)
    new_block = node1_blockchain.mine()

    # Maintenant, new_block ne sera plus None
    success = node2_blockchain.integrate_block(new_block)

    assert success is True
    assert node1_blockchain.chain == node2_blockchain.chain