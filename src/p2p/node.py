import socket
import threading
import json


class P2PNode:
    def __init__(self, blockchain, host='0.0.0.0', port=5000):
        self.blockchain = blockchain
        self.host = host
        self.port = port
        self.peers = []

    def connect_to_peer(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            self.peers.append(s)
            threading.Thread(target=self.handle_client, args=(s,), daemon=True).start()
            print(f"[P2P] Connecté au pair {host}:{port}")
        except Exception as e:
            print(f"[P2P] Erreur de connexion : {e}")

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[P2P] Serveur lancé sur {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            print(f"[P2P] Nouvelle connexion de {addr}")
            self.peers.append(conn)  # On sauvegarde la connexion pour broadcast
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        while True:
            try:
                msg = conn.recv(4096).decode()
                if not msg: break

                # Sécurité : on vérifie que c'est du JSON valide
                try:
                    payload = json.loads(msg)
                except json.JSONDecodeError:
                    print(f"[P2P] Reçu message non-JSON : {msg}")
                    continue

                if payload.get("type") == "NEW_TRANSACTION":
                    self.handle_transaction(payload["data"])
                elif payload.get("type") == "NEW_BLOCK":
                    self.handle_block(payload["data"])
                else:
                    print(f"[P2P] Message inconnu reçu : {payload}")

            except Exception as e:
                print(f"[P2P] Erreur de lecture : {e}")
                break
        conn.close()

    def handle_transaction(self, data):
        from src.core.transaction import Transaction  # Import local pour éviter les imports circulaires

        # On vérifie si on n'a pas déjà cette transaction pour éviter de boucler à l'infini
        # (Simple check : si elle est déjà dans la mempool, on ne fait rien)
        if data in self.blockchain.mempool:
            return

        tx = Transaction(
            data['sender'],
            data['receiver'],
            data['amount'],
            data['signature']
        )

        if self.blockchain.add_transaction(tx):
            print(f"[P2P] Transaction relayée : {data['amount']} SAD")
            # On ne broadcast QUE si c'est une nouvelle transaction pour nous
            self.broadcast("NEW_TRANSACTION", data)

    def broadcast(self, message_type, data):
        """Envoie un message à tous les pairs connectés."""
        payload = json.dumps({"type": message_type, "data": data})
        for peer in self.peers:
            try:
                peer.send(payload.encode())
            except:
                self.peers.remove(peer)

    def handle_block(self, block_data):
        # Utilise la blockchain passée à l'initialisation
        if self.blockchain.integrate_block(block_data):
            print(f"[P2P] Bloc validé et ajouté : {block_data.get('hash')}")
        else:
            print("[P2P] ALERTE : Bloc invalide reçu !")