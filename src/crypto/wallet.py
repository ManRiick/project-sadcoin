import hashlib
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_der


class Wallet:
    """
    Represents a blockchain participant's identity.
    Handles key pair generation, address derivation, and transaction signing.
    """

    def __init__(self):
        # Generate a new private key using the SECP256k1 elliptic curve (Bitcoin standard)
        self._private_key = SigningKey.generate(curve=SECP256k1)
        # Derive the corresponding public key from the private key
        self._public_key = self._private_key.get_verifying_key()

    def get_address(self) -> str:
        """
        Returns the wallet address as a hexadecimal string.
        In this implementation, the address is the uncompressed public key.
        """
        return self._public_key.to_string().hex()

    def sign_transaction(self, message: str) -> str:
        """
        Signs a message using the private key to prove ownership and intent.

        Args:
            message (str): The transaction data to be signed.

        Returns:
            str: The digital signature in hexadecimal format (DER encoded).
        """
        # Using sigencode_der ensures compatibility with JavaScript elliptic libraries.
        return self._private_key.sign(
            message.encode(),
            hashfunc=hashlib.sha256,
            sigencode=sigencode_der  # Standardized encoding for cross-platform verification
        ).hex()