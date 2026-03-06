import socket
import json
import requests
import hashlib
from src.crypto.wallet import Wallet


def send_money():
    """
    Simulation of a client-side transaction:
    Generates keys, signs a payload, and submits it to the blockchain API.
    """

    # 1. Identity Initialization
    sender = Wallet()
    receiver_address = "test_address_12345"
    amount = 50

    # Extract the public key in hex format to act as the sender's address
    sender_pub = sender._public_key.to_string().hex()

    # 2. Message Construction
    # The message must be concatenated in the exact same order as the verification logic
    message = f"{sender_pub}{receiver_address}{amount}"

    # Generate a SHA-256 hash of the message to be signed
    hash_msg = hashlib.sha256(message.encode()).hexdigest()

    #
    # 3. Cryptographic Signing
    # The private key signs the hash of the message to prove authorization
    signature = sender._private_key.sign(hash_msg.encode()).hex()

    # 4. Data Packaging
    # Construct the JSON payload required by the /send endpoint
    tx = {
        "sender": sender_pub,
        "receiver": receiver_address,
        "amount": amount,
        "signature": signature
    }

    # 5. API Submission
    # Send the signed transaction to a local node (Client 1) via HTTP POST
    try:
        r = requests.post(
            "http://localhost:8081/send",
            json=tx
        )
        # Display the server's response (Success or Validation Error)
        print(f"Server Response: {r.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Node API. Is Docker running?")


if __name__ == "__main__":
    send_money()