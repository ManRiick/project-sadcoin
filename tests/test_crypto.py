import pytest
from src.crypto.wallet import Wallet


def test_wallet_address_generation():
    wallet = Wallet()
    address = wallet.get_address()
    assert len(address) == 64  # Le hash SHA256 fait 64 caractères hexadécimaux


def test_signature_verification():
    wallet = Wallet()
    data = "Transaction de 10 coins"

    # Signer
    signature = wallet.sign_transaction(data)

    # Vérifier
    is_valid = Wallet.verify_signature(
        wallet._public_key.to_string(),
        signature,
        data
    )
    assert is_valid is True


def test_invalid_signature():
    wallet = Wallet()
    data = "Données originales"
    tampered_data = "Données modifiées"

    signature = wallet.sign_transaction(data)

    # Vérifier avec des données modifiées -> Doit échouer
    is_valid = Wallet.verify_signature(
        wallet._public_key.to_string(),
        signature,
        tampered_data
    )
    assert is_valid is False