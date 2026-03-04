# tests/test_network.py
from src.core.transaction import Transaction
from src.crypto.wallet import Wallet
from src.core.blockchain import Blockchain


def test_full_transaction_flow():
    # Setup
    blockchain = Blockchain()
    wallet = Wallet()
    receiver = "fake_address"
    amount = 10

    # Action
    sender_pub = wallet._public_key.to_string().hex()
    data = f"{sender_pub}{receiver}{amount}"
    signature = wallet.sign_transaction(data)
    tx = Transaction(sender_pub, receiver, amount, signature)

    # Vérification
    assert blockchain.add_transaction(tx) is True
    assert len(blockchain.mempool) == 1