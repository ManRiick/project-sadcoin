import socket
import json
import requests
import hashlib
from src.crypto.wallet import Wallet

def send_money():

    sender = Wallet()
    receiver_address = "adresse_de_test_12345"
    amount = 50

    sender_pub = sender._public_key.to_string().hex()

    message = f"{sender_pub}{receiver_address}{amount}"
    hash_msg = hashlib.sha256(message.encode()).hexdigest()

    signature = sender._private_key.sign(hash_msg.encode()).hex()

    tx = {
        "sender": sender_pub,
        "receiver": receiver_address,
        "amount": amount,
        "signature": signature
    }

    r = requests.post(
        "http://localhost:8081/send",
        json=tx
    )

    print(r.json())

send_money()