import hashlib
import time
import json
from src.core.transaction import Transaction


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.mempool = []  # <--- Ta file d'attente !
        self.difficulty = 4  # Nombre de zéros requis au début du hash

    def create_genesis_block(self):
        return {"index": 0, "hash": "0", "prev_hash": "0", "nonce": 0, "transactions": []}

    def add_transaction(self, tx: Transaction):
        if tx.verify():  # On vérifie avant d'ajouter !
            self.mempool.append(tx.to_dict())
            return True
        return False

    def mine(self):
        """Transforme la mempool en un nouveau bloc."""
        if not self.mempool:
            return None

        last_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "transactions": self.mempool,
            "prev_hash": last_block["hash"],
            "nonce": 0
        }

        # --- Proof of Work ---
        while True:
            block_string = json.dumps(new_block, sort_keys=True).encode()
            new_block["hash"] = hashlib.sha256(block_string).hexdigest()

            # Vérification de la difficulté (ex: commence par "0000")
            if new_block["hash"][:self.difficulty] == "0" * self.difficulty:
                break
            new_block["nonce"] += 1

        self.chain.append(new_block)
        self.mempool = []  # On vide la mempool après le minage
        return new_block

    def validate_block(self, block):
        """Vérifie si un bloc reçu est valide."""
        last_block = self.chain[-1]

        # 1. Vérifier le lien avec le précédent (La continuité)
        if block["prev_hash"] != last_block["hash"]:
            return False

        # 2. Vérifier le hash (Le PoW)
        # On recalcule le hash du bloc reçu pour voir s'il correspond aux critères
        block_string = json.dumps(block, sort_keys=True).encode()
        calculated_hash = hashlib.sha256(block_string).hexdigest()

        # Le hash doit commencer par tes zéros (difficulté)
        if calculated_hash[:self.difficulty] != "0" * self.difficulty:
            return False

        return True

    def integrate_block(self, block):
        """Ajoute le bloc à la chaîne et vide la mempool locale."""
        if self.validate_block(block):
            self.chain.append(block)
            # On retire de la mempool les transactions qui ont été minées
            # (Simplification : on vide tout ce qu'on a déjà)
            self.mempool = []
            print("[BLOCKCHAIN] Nouveau bloc intégré avec succès !")
            return True
        return False