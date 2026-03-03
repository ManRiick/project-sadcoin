import socket
import threading
import json


class P2PNode:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.peers = []  # Liste des connexions actives

    def start_server(self):
        """Lance le serveur qui écoute les autres nœuds."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[P2P] Serveur lancé sur {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            print(f"[P2P] Nouvelle connexion de {addr}")
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        """Gère les messages reçus."""
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data: break
                print(f"[P2P] Message reçu : {data}")
            except:
                break
        conn.close()

    def connect_to_peer(self, peer_host, peer_port):
        """Se connecte à un autre nœud (ex: system-node:5000)."""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((peer_host, int(peer_port)))
            self.peers.append(client)
            print(f"[P2P] Connecté à {peer_host}:{peer_port}")
            client.send("Hello du Sadcoin !".encode())
        except Exception as e:
            print(f"[P2P] Erreur de connexion : {e}")