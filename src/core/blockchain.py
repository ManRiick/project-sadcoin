import hashlib
import time
import json
from src.core.transaction import Transaction


class Blockchain:
    """
    Core Blockchain engine managing the ledger, transaction mempool,
    and the Proof of Work consensus mechanism.
    """

    def __init__(self):
        # Initialize the chain with the hardcoded Genesis Block
        self.chain = [self.create_genesis_block()]
        # Temporary storage for validated transactions awaiting inclusion in a block
        self.mempool = []
        # Difficulty level: Number of leading zeros required for a valid block hash
        self.difficulty = 4

    def create_genesis_block(self):
        """Generates the initial block of the blockchain (Block #0)."""
        return {
            "index": 0,
            "hash": "0",
            "prev_hash": "0",
            "nonce": 0,
            "transactions": []
        }

    def add_transaction(self, tx: Transaction):
        """
        Validates the transaction signature before adding it to the mempool.
        Ensures only authentic transactions are queued for mining.
        """
        if tx.verify():  # Cryptographic signature verification
            self.mempool.append(tx.to_dict())
            return True
        return False

    def mine(self):
        """
        Executes the Proof of Work algorithm to seal the current mempool into a new block.
        """
        if not self.mempool:
            return None

        last_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "transactions": self.mempool,
            "prev_hash": last_block["hash"],
            "nonce": 0,
            "hash": None  # Will be populated once the winning hash is found
        }

        #
        # Mining loop: Increment nonce until the hash meets the difficulty target
        while True:
            # Create a shallow copy to calculate hash excluding the hash field itself
            calc_block = new_block.copy()
            calc_block.pop("hash")

            # Deterministic serialization (sort_keys) ensures consistent hashing
            block_string = json.dumps(calc_block, sort_keys=True).encode()
            current_hash = hashlib.sha256(block_string).hexdigest()

            # Check if the hash satisfies the network difficulty requirement
            if current_hash[:self.difficulty] == "0" * self.difficulty:
                new_block["hash"] = current_hash  # Winning hash found
                break
            new_block["nonce"] += 1

        # Append the successfully mined block to the ledger and clear the local mempool
        self.chain.append(new_block)
        self.mempool = []
        return new_block

    def validate_block(self, block):
        """
        Validates a block received from the network by checking hash continuity
        and verifying the Proof of Work.
        """
        last_block = self.chain[-1]

        # 1. Chain Continuity Check: Ensure the block references the correct previous hash
        if block["prev_hash"] != last_block["hash"]:
            return False

        # 2. Proof of Work Verification: Recalculate the hash to confirm its validity
        # Create a temporary copy to avoid modifying the original block data
        temp_block = block.copy()
        received_hash = temp_block.pop("hash")  # Extract the hash for comparison

        #
        # Re-hash the block data using the same deterministic method as the miner
        block_string = json.dumps(temp_block, sort_keys=True).encode()
        calculated_hash = hashlib.sha256(block_string).hexdigest()

        # Block is valid if the hash matches the data and meets the difficulty target
        return (calculated_hash == received_hash and
                calculated_hash[:self.difficulty] == "0" * self.difficulty)

    def integrate_block(self, block):
        """
        Validates and appends a block mined by a peer to the local chain.
        Synchronizes the local node with the network state.
        """
        if self.validate_block(block):
            self.chain.append(block)
            # Flush mempool to prevent double-processing of included transactions
            self.mempool = []
            print("[BLOCKCHAIN] New block successfully integrated!")
            return True
        return False