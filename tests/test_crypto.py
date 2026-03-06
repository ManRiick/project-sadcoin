import pytest
import hashlib

from ecdsa import VerifyingKey, SECP256k1

from src.crypto.wallet import Wallet
from ecdsa.util import sigencode_der, sigdecode_der
from src.core.transaction import Transaction
from src.core.blockchain import Blockchain


# --- TESTS CRYPTO ---

def test_wallet_address_generation():
    wallet = Wallet()
    address = wallet.get_address()
    # Une clé publique SECP256k1 brute fait 64 bytes (128 caractères hex)
    # Si tu as suivi mon conseil précédent sur l'adresse = clé publique
    assert len(address) == 128


def test_signature_integrity():
    wallet = Wallet()
    data = "Message Secret"
    signature_hex = wallet.sign_transaction(data)

    # Récupération de la clé publique depuis l'adresse hex
    public_key_bytes = bytes.fromhex(wallet.get_address())
    vk = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)

    # On vérifie : ça doit passer maintenant !
    assert vk.verify(
        bytes.fromhex(signature_hex),
        data.encode(),
        hashfunc=hashlib.sha256,
        sigdecode=sigdecode_der
    )

# --- TESTS BLOCKCHAIN ---

def test_blockchain_pow_difficulty():
    bc = Blockchain()
    bc.mempool = [{"sender": "A", "receiver": "B", "amount": 10}]  # Simulation
    block = bc.mine()

    # On vérifie que le hash respecte bien la difficulté (ex: 4 zéros)
    assert block["hash"].startswith("0" * bc.difficulty)


def test_invalid_transaction_rejected():
    bc = Blockchain()
    # Transaction sans signature
    tx = Transaction("sender", "receiver", 10, None)
    assert bc.add_transaction(tx) is False
    assert len(bc.mempool) == 0


def test_blockchain_tampering():
    bc = Blockchain()
    bc.mempool = [{"sender": "A", "receiver": "B", "amount": 10}]
    block = bc.mine()

    # On tente de modifier une transaction dans le bloc APRES le minage
    block["transactions"][0]["amount"] = 1000000

    # La validation doit échouer car le hash ne correspond plus
    assert bc.validate_block(block) is False