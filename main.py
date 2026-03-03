import os
import time


def main():
    node_name = os.getenv("NODE_NAME", "Unknown")
    print(f"--- [SADCOIN] Démarrage du nœud : {node_name} ---")

    # Ici, plus tard, tu appelleras ton moteur blockchain
    # from src.core.blockchain import Blockchain
    # blockchain = Blockchain()

    while True:
        print(f"Le nœud {node_name} est en attente de connexions P2P...")
        time.sleep(10)  # Simule une boucle d'exécution


if __name__ == "__main__":
    main()