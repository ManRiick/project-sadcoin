import os
import threading
import time
from src.crypto.wallet import Wallet
from src.p2p.node import P2PNode

def main():
    # 1. Identité du nœud
    node_name = os.getenv("NODE_NAME", "Unknown")
    my_port = int(os.getenv("MY_PORT", 5000))
    peers_str = os.getenv("PEERS", "")

    # Initialisation du Wallet
    wallet = Wallet()
    print(f"--- [SADCOIN] Démarrage du nœud : {node_name} ---")
    print(f"--- [WALLET] Adresse générée : {wallet.get_address()[:20]}... ---")

    # 2. Serveur P2P
    node = P2PNode(port=my_port)
    server_thread = threading.Thread(target=node.start_server, daemon=True)
    server_thread.start()

    # 3. Connexion au réseau (Test Ultime)
    if peers_str:
        time.sleep(2) # On attend que le système soit prêt
        for peer in peers_str.split(','):
            host, port = peer.split(':')
            print(f"--- [P2P] Tentative de connexion à {host}:{port} ---")
            node.connect_to_peer(host, int(port))

    # Garder le thread principal actif
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Arrêt du nœud...")

if __name__ == "__main__":
    main()