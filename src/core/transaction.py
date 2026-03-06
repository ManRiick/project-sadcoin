import hashlib
from ecdsa import VerifyingKey, SECP256k1
from ecdsa.util import sigdecode_der


class Transaction:
    def __init__(self, sender_pub_key, receiver_pub_key, amount, signature=None):
        self.sender = sender_pub_key
        self.receiver = receiver_pub_key
        self.amount = amount
        self.signature = signature

    def verify(self):
        if not self.signature:
            return False

        # On recrée exactement la même chaîne qu'en JS
        # IMPORTANT : amount doit être converti en string
        message = f"{self.sender}{self.receiver}{self.amount}".encode()

        try:
            # On récupère la clé publique (128 caractères hex = 64 bytes)
            vk = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)

            # On vérifie en précisant explicitement hashlib.sha256
            return vk.verify(
                bytes.fromhex(self.signature),
                message,
                hashfunc=hashlib.sha256,  # Crucial pour la compatibilité avec JS
                sigdecode=sigdecode_der
            )
        except Exception as e:
            print(f"VERIFY ERROR: {e}")
            return False

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "signature": self.signature
        }