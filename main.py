import os
import threading
import time

from src.core.blockchain import Blockchain
from src.crypto.wallet import Wallet
from src.p2p.node import P2PNode
from src.api.app import run_api

def main():
    """
    Main entry point for the SadCoin Node.
    Orchestrates the Blockchain engine, P2P networking, and the Flask API.
    """
    # 1. Node Configuration
    # Retrieve settings from environment variables (ideal for Docker Compose)
    node_name = os.getenv("NODE_NAME", "Unknown")
    my_port = int(os.getenv("MY_PORT", 5000))
    peers_str = os.getenv("PEERS", "")

    # Initialization of core components
    my_blockchain = Blockchain()
    node = P2PNode(blockchain=my_blockchain, port=my_port)

    # Wallet identity initialization
    wallet = Wallet()
    print(f"--- [SADCOIN] Starting node: {node_name} ---")
    print(f"--- [WALLET] Address generated: {wallet.get_address()[:20]}... ---")

    #
    # 2. Concurrency Management
    # Start the P2P server and the Flask Web API in separate daemon threads
    server_thread = threading.Thread(target=node.start_server, daemon=True)
    threading.Thread(target=run_api, args=(node,), daemon=True).start()
    server_thread.start()

    # 3. Network Discovery and Connection
    # If peer addresses are provided, attempt to join the existing network
    if peers_str:
        # Grace period to ensure local servers are fully initialized before connecting
        time.sleep(2)
        for peer in peers_str.split(','):
            try:
                host, port = peer.split(':')
                print(f"--- [P2P] Attempting to connect to {host}:{port} ---")
                node.connect_to_peer(host, int(port))
            except ValueError:
                print(f"--- [P2P] Invalid peer format: {peer} ---")

    # Keep the main thread alive to maintain the background processes
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopping node...")

if __name__ == "__main__":
    main()