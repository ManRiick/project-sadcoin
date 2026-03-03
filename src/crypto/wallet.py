from ecdsa import SigningKey, SECP256k1
import hashlib


class Wallet:
    def __init__(self):
        # Générer une clé privée (la signature)
        self._private_key = SigningKey.generate(curve=SECP256k1)
        # Générer la clé publique (l'adresse)
        self._public_key = self._private_key.get_verifying_key()

    def get_address(self) -> str:
        # L'adresse est le hash de la clé publique
        pub_key_bytes = self._public_key.to_string()
        return hashlib.sha256(pub_key_bytes).hexdigest()

    def sign_transaction(self, data: str) -> str:
        # Signer des données avec la clé privée
        return self._private_key.sign(data.encode()).hex()
