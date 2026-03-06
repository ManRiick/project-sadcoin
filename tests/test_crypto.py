import pytest
import hashlib

from ecdsa import VerifyingKey, SECP256k1

from src.crypto.wallet import Wallet
from ecdsa.util import sigencode_der, sigdecode_der
from src.core.transaction import Transaction
from src.core.blockchain import Blockchain


# --- CRYPTOGRAPHY TESTS ---

def test_wallet_address_generation():
    """Verifies that the wallet generates a valid SECP256k1 public key address."""
    wallet = Wallet()
    address = wallet.get_address()
    # A raw SECP256k1 public key consists of 64 bytes (128 hex characters).
    # This assertion ensures the address format is correct for our protocol.
    assert len(address) == 128


def test_signature_integrity():
    """Validates the digital signature process and its cross-platform compatibility."""
    wallet = Wallet()
    data = "Secret Message"
    signature_hex = wallet.sign_transaction(data)

    # Reconstruct the public key object from the hex address string
    public_key_bytes = bytes.fromhex(wallet.get_address())
    vk = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)

    # Verification must pass using SHA256 and DER decoding to ensure
    # interoperability between the wallet and the transaction logic.
    assert vk.verify(
        bytes.fromhex(signature_hex),
        data.encode(),
        hashfunc=hashlib.sha256,
        sigdecode=sigdecode_der
    )

# --- BLOCKCHAIN TESTS ---

def test_blockchain_pow_difficulty():
    """Ensures the mining process respects the network's Proof of Work difficulty."""
    bc = Blockchain()
    bc.mempool = [{"sender": "A", "receiver": "B", "amount": 10}]  # Mock transaction
    block = bc.mine()

    # The resulting hash must start with the exact number of zeros defined by difficulty
    assert block["hash"].startswith("0" * bc.difficulty)


def test_invalid_transaction_rejected():
    """Verifies that unsigned or malformed transactions cannot enter the mempool."""
    bc = Blockchain()
    # Attempting to add a transaction missing a signature
    tx = Transaction("sender", "receiver", 10, None)
    assert bc.add_transaction(tx) is False
    assert len(bc.mempool) == 0


def test_blockchain_tampering():
    """Tests the immutability of the blockchain by attempting to modify mined data."""
    bc = Blockchain()
    bc.mempool = [{"sender": "A", "receiver": "B", "amount": 10}]
    block = bc.mine()

    # Simulation of a '51% attack' or local tampering: modifying data AFTER mining
    block["transactions"][0]["amount"] = 1000000

    # The block validation must fail because the hash is no longer cryptographically linked to the data
    assert bc.validate_block(block) is False