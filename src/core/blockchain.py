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

    # Modifie ces deux méthodes dans Blockchain

    def mine(self):
        if not self.mempool:
            return None

        last_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "transactions": self.mempool,
            "prev_hash": last_block["hash"],
            "nonce": 0,
            "hash": None  # On initialise à None
        }

        while True:
            # On crée une copie pour le calcul sans le champ hash
            calc_block = new_block.copy()
            calc_block.pop("hash")

            block_string = json.dumps(calc_block, sort_keys=True).encode()
            current_hash = hashlib.sha256(block_string).hexdigest()

            if current_hash[:self.difficulty] == "0" * self.difficulty:
                new_block["hash"] = current_hash  # On stocke le hash gagnant
                break
            new_block["nonce"] += 1

        self.chain.append(new_block)
        self.mempool = []
        return new_block

    def validate_block(self, block):
        last_block = self.chain[-1]
        if block["prev_hash"] != last_block["hash"]:
            return False

        # Recalculer pour vérifier le PoW
        check_block = block.copy()
        received_hash = check_block.pop("hash")  # On extrait le hash pour vérifier le reste

        block_string = json.dumps(check_block, sort_keys=True).encode()
        calculated_hash = hashlib.sha256(block_string).hexdigest()

        return calculated_hash == received_hash and calculated_hash[:self.difficulty] == "0" * self.difficulty

    def validate_block(self, block):
        last_block = self.chain[-1]
        if block["prev_hash"] != last_block["hash"]:
            return False

        # Créer une copie pour ne pas modifier l'original
        temp_block = block.copy()
        received_hash = temp_block.pop("hash")  # On retire le hash pour recalculer

        block_string = json.dumps(temp_block, sort_keys=True).encode()
        calculated_hash = hashlib.sha256(block_string).hexdigest()

        return calculated_hash == received_hash and calculated_hash[:self.difficulty] == "0" * self.difficulty

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