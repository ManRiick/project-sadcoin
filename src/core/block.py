import hashlib
import time

class Block:
    def __init__(self, index, transactions, prev_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # On concatène tout pour créer une empreinte unique
        block_content = f"{self.index}{self.timestamp}{self.transactions}{self.prev_hash}{self.nonce}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine(self, difficulty):
        # La difficulté = nombre de zéros requis au début du hash
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Bloc miné ! Hash : {self.hash}")