import json
from src.crypto.wallet import Wallet


class Transaction:
    def __init__(self, sender_pub_key, receiver_pub_key, amount, signature=None):
        self.sender = sender_pub_key  # Clé publique de l'expéditeur (hex)
        self.receiver = receiver_pub_key  # Clé publique du destinataire (hex)
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        """Transforme la transaction en dictionnaire pour le réseau (JSON)."""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "signature": self.signature
        }

    def verify(self):
        """
        Vérifie si la signature est valide.
        Cette méthode utilise ta classe Wallet pour valider l'intégrité.
        """
        if not self.signature:
            return False

        # Reconstruire le message original qui a été signé
        # IMPORTANT: il doit être identique à ce qui a été signé au départ
        msg = f"{self.sender}{self.receiver}{self.amount}"

        return Wallet.verify_signature(
            public_key_bytes=bytes.fromhex(self.sender),
            signature_hex=self.signature,
            data=msg
        )