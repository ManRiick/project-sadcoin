from ecdsa import SigningKey, SECP256k1, VerifyingKey
import hashlib


class Wallet:
    def __init__(self):
        # Générer une clé privée
        self._private_key = SigningKey.generate(curve=SECP256k1)
        # Générer la clé publique
        self._public_key = self._private_key.get_verifying_key()

    def get_address(self) -> str:
        # L'adresse est le hash de la clé publique
        pub_key_bytes = self._public_key.to_string()
        return hashlib.sha256(pub_key_bytes).hexdigest()

    def sign_transaction(self, data: str) -> str:
        # Signer des données avec la clé privée
        return self._private_key.sign(data.encode()).hex()

    @staticmethod
    def verify_signature(public_key_bytes: bytes, signature_hex: str, data: str) -> bool:
        """
        Vérifie si une signature est valide pour des données données.
        public_key_bytes : la clé publique (en bytes) de celui qui a signé
        signature_hex : la signature reçue (en hexadécimal)
        data : le message original qui a été signé
        """
        try:
            # 1. On transforme les bytes en objet clé de vérification
            vk = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)

            # 2. On vérifie la signature (on convertit l'hex en bytes)
            return vk.verify(bytes.fromhex(signature_hex), data.encode())
        except Exception as e:
            # Si ça échoue (signature corrompue, clé invalide...), c'est faux
            return False