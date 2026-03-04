import pytest
from src.core.transaction import Transaction
from src.crypto.wallet import Wallet


def test_transaction_lifecycle():
    # 1. Setup : Création des acteurs
    sender_wallet = Wallet()
    receiver_wallet = Wallet()

    sender_pub_key = sender_wallet._public_key.to_string().hex()
    receiver_pub_key = receiver_wallet._public_key.to_string().hex()
    amount = 50

    # 2. Création de la transaction (Data = sender + receiver + amount)
    data = f"{sender_pub_key}{receiver_pub_key}{amount}"
    signature = sender_wallet.sign_transaction(data)

    tx = Transaction(sender_pub_key, receiver_pub_key, amount, signature)

    # 3. Test : La transaction doit être valide
    assert tx.verify() is True


def test_transaction_tampering():
    # 1. Setup
    sender_wallet = Wallet()
    receiver_wallet = Wallet()
    sender_pub_key = sender_pub_key = sender_wallet._public_key.to_string().hex()
    receiver_pub_key = receiver_wallet._public_key.to_string().hex()

    # 2. On crée une transaction honnête...
    amount = 50
    data = f"{sender_pub_key}{receiver_pub_key}{amount}"
    signature = sender_wallet.sign_transaction(data)
    tx = Transaction(sender_pub_key, receiver_pub_key, amount, signature)

    # 3. ... mais on triche ! On modifie le montant sans refaire la signature
    tx.amount = 999999

    # 4. Test : La vérification doit échouer
    assert tx.verify() is False