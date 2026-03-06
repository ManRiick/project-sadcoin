import hashlib

from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_der


class Wallet:
    def __init__(self):
        self._private_key = SigningKey.generate(curve=SECP256k1)
        self._public_key = self._private_key.get_verifying_key()

    def get_address(self) -> str:
        # On garde la clé publique en hex pour l'adresse (format non compressé)
        return self._public_key.to_string().hex()

    def sign_transaction(self, message: str) -> str:
        # On ajoute sigencode=sigencode_der pour être compatible avec le JS
        return self._private_key.sign(
            message.encode(),
            hashfunc=hashlib.sha256,
            sigencode=sigencode_der  # <--- CRUCIAL : Génère du format DER
        ).hex()