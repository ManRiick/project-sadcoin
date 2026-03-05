import socket
import json
from src.crypto.wallet import Wallet
from src.core.transaction import Transaction


def send_money():
    # 1. On prépare les acteurs
    sender = Wallet()
    receiver_address = "adresse_de_test_12345"
    amount = 50

    # 2. Création de la transaction signée
    sender_pub = sender._public_key.to_string().hex()
    data = f"{sender_pub}{receiver_address}{amount}"
    signature = sender.sign_transaction(data)

    tx_data = {
        "sender": sender_pub,
        "receiver": receiver_address,
        "amount": amount,
        "signature": signature
    }

    # 3. On l'envoie au CLIENT_1 (qui tourne sur Docker)
    # Note : Sur Windows, localhost redirige vers Docker si les ports sont mappés
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 5001))  # Port de CLIENT_1
            s.sendall(json.dumps({"type": "NEW_TRANSACTION", "data": tx_data}).encode())
            print("✅ Transaction envoyée au réseau !")
    except Exception as e:
        print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    send_money()