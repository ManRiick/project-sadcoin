import socket
import threading
import json


class P2PNode:
    """
    Handles Peer-to-Peer networking, enabling nodes to communicate,
    synchronize the blockchain, and propagate transactions.
    """
    def __init__(self, blockchain, host='0.0.0.0', port=5000):
        self.blockchain = blockchain
        self.host = host
        self.port = port
        self.peers = []  # List of active socket connections to other nodes

    def connect_to_peer(self, host, port):
        """Established an outbound connection to a specific peer."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            self.peers.append(s)
            # Start a background thread to listen for messages from this specific peer
            threading.Thread(target=self.handle_client, args=(s,), daemon=True).start()
            print(f"[P2P] Connected to peer {host}:{port}")
        except Exception as e:
            print(f"[P2P] Connection error: {e}")

    def start_server(self):
        """Starts the inbound TCP server to accept connections from other nodes."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow immediate reuse of the port after restart
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[P2P] Server listening on {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            print(f"[P2P] New inbound connection from {addr}")
            self.peers.append(conn)
            # Handle each connection in a separate thread to maintain concurrency
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        """Continuously listens for incoming data from a specific peer connection."""
        while True:
            try:
                msg = conn.recv(4096).decode()
                if not msg: break

                # Data integrity: Ensure the received message is valid JSON
                try:
                    payload = json.loads(msg)
                except json.JSONDecodeError:
                    print(f"[P2P] Received non-JSON message: {msg}")
                    continue

                # Route the message based on its 'type' attribute
                if payload.get("type") == "NEW_TRANSACTION":
                    self.handle_transaction(payload["data"])
                elif payload.get("type") == "NEW_BLOCK":
                    self.handle_block(payload["data"])
                else:
                    print(f"[P2P] Unknown message type received: {payload}")

            except Exception as e:
                print(f"[P2P] Read error: {e}")
                break
        conn.close()

    def handle_transaction(self, data):
        """Processes and relays new transactions across the network."""
        from src.core.transaction import Transaction  # Local import to prevent circular dependency

        # Prevent infinite loops: Do nothing if the transaction is already in our mempool
        if data in self.blockchain.mempool:
            return

        tx = Transaction(
            data['sender'],
            data['receiver'],
            data['amount'],
            data['signature']
        )

        # If valid, add to local mempool and relay to other connected peers (Gossip protocol)
        if self.blockchain.add_transaction(tx):
            print(f"[P2P] Transaction relayed: {data['amount']} SAD")
            self.broadcast("NEW_TRANSACTION", data)

    def broadcast(self, message_type, data):
        """Sends a message to every connected peer in the network."""
        payload = json.dumps({"type": message_type, "data": data})
        for peer in self.peers:
            try:
                peer.send(payload.encode())
            except:
                # Cleanup disconnected peers to maintain network health
                self.peers.remove(peer)

    def handle_block(self, block_data):
        """Validates and integrates new blocks received from the network."""
        if self.blockchain.integrate_block(block_data):
            print(f"[P2P] Block validated and added to chain: {block_data.get('hash')}")
        else:
            print("[P2P] WARNING: Received invalid block!")