
def is_chain_valid(self):
    for i in range(1, len(self.chain)):
        current_block = self.chain[i]
        prev_block = self.chain[i - 1]

        # 1. Vérifier si le hash actuel est toujours correct
        if current_block.hash != current_block.calculate_hash():
            return False

        # 2. Vérifier si le lien avec le bloc précédent est intact
        if current_block.prev_hash != prev_block.hash:
            return False

    return True