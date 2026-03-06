import hashlib
from ecdsa import VerifyingKey, SECP256k1
from ecdsa.util import sigdecode_der


class Transaction:
    """
    Represents a value transfer between two peers on the blockchain.
    Handles data structure and integrity validation via ECDSA digital signatures.
    """
    def __init__(self, sender_pub_key, receiver_pub_key, amount, signature=None):
        self.sender = sender_pub_key      # Sender's public key (Wallet Address)
        self.receiver = receiver_pub_key  # Receiver's public key
        self.amount = amount              # Amount to be transferred
        self.signature = signature        # Digital signature in DER hex format

    def verify(self):
        """
        Validates the transaction's authenticity by verifying the signature
        against the sender's public key.
        """
        if not self.signature:
            return False

        #
        # Deterministic reconstruction of the original message payload.
        # CRITICAL: This must match the exact string format used in the JS frontend.
        message = f"{self.sender}{self.receiver}{self.amount}".encode()

        try:
            # Reconstruct the VerifyingKey object from the hexadecimal string.
            # Using SECP256k1 curve (Industrial standard used by Bitcoin).
            vk = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)

            #
            # Cryptographic validation using the ECDSA algorithm.
            # Explicitly defining hashlib.sha256 and sigdecode_der ensures
            # full compatibility between the Python backend and JavaScript elliptic library.
            return vk.verify(
                bytes.fromhex(self.signature),
                message,
                hashfunc=hashlib.sha256,  # Matching the hash function used for signing
                sigdecode=sigdecode_der   # Decoding the ASN.1 DER format
            )
        except Exception as e:
            # Logging validation failures (e.g., malformed signature or invalid key format)
            print(f"VERIFY ERROR: {e}")
            return False

    def to_dict(self):
        """
        Converts the Transaction object into a dictionary for JSON serialization
        and inclusion within blockchain blocks.
        """
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "signature": self.signature
        }