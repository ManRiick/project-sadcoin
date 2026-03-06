# 🛡️ SadCoin : A Blockchain for Understanding
*Texte français au-dessous*

SadCoin is a lightweight implementation of a decentralized blockchain using Proof of Work, a P2P (Peer-to-Peer) architecture, and an interactive web interface.

### 🚀 Features:

**Elliptic Curve Cryptography:** Transaction signing and verification with the secp256k1 curve (Bitcoin standard).

**Consensus:** Mining via Proof of Work (PoW) with adjustable difficulty.

**P2P Networking:** Automatic propagation of transactions and new blocks between nodes via Docker.

**Web Interface:** JS-integrated Wallet to create addresses, send funds, and monitor the chain.

**Automated Testing:** Unit test suite with pytest integrated into the Docker build.

### 🛠️ Architecture du Système
The project relies on three pillars:

**The Core (Python):** Manages the chain logic, block validation, and the mempool.

**The P2P Layer:** Manages sockets to connect nodes to each other.

**The Flask API:** Bridges the blockchain and the user interface.

### 📦 Installation and Launch (Docker)
The recommended method is to use Docker Compose to simulate a 3-node network on your machine.

1. Prerequisites

    Docker and Docker Compose installed. 
    Python 3.13 (if you want to run tests locally).

2. Starting the network

*Build and launch the 3 nodes (System, Client 1, Client 2)*

```docker-compose up --build ```

3. Accessing the interfaces
Each node exposes its own web wallet on a different port:

* System Node: http://localhost:8080

* Client 1: http://localhost:8081

* Client 2: http://localhost:8082

### 🧪 Unit Testing
Tests are automatically launched during the docker build. To run them manually in your virtual environment:

``` pytest tests/ ```

**What is tested:**

* Key and address generation.

* DER signature integrity (Python/JS compatibility).

* Proof of Work validation (leading zeros).

* Block synchronization between two blockchain instances.

### 📝 User Guide
1. **Create a Wallet:** Click "Create wallet" on Client 1 and Client 2.
2. **Transaction:** Copy Client 2's address, paste it into Client 1's interface, enter an amount, and send.
3. **Propagation:** The transaction appears instantly in the Mempool of both clients.
4. **Mining:** Click "Mine block". A new block is generated, validated by the network, and added to the Blockchain visible at the bottom of the page.

### ⚠️ Security and Limitations
* **No Persistence:** The chain is stored in memory (RAM). Restarting Docker resets the blockchain.

* **Double Spending:** The balance system is simplified and does not yet verify UTXOs (Unspent Transaction Outputs) in real-time before adding to the mempool.

---
# 🛡️ SadCoin : Une Blockchain pour comprendre 
*English text below*

SadCoin est une implémentation légère d'une blockchain décentralisée utilisant la preuve de travail (Proof of Work), une architecture P2P (Peer-to-Peer) et une interface web interactive.

### 🚀 Fonctionnalités:

**Cryptographie Elliptique :** Signature et vérification des transactions avec la courbe secp256k1 (standard Bitcoin).

**Consensus :** Minage par Preuve de Travail (PoW) avec difficulté ajustable.

**Réseau P2P :** Propagation automatique des transactions et des nouveaux blocs entre les nœuds via Docker.

**Interface Web :** Wallet intégré en JS pour créer des adresses, envoyer des fonds et surveiller la chaîne.

**Tests Automatisés :** Suite de tests unitaires avec pytest intégrée au build Docker.

### 🛠️ Architecture du Système
Le projet repose sur trois piliers :

**Le Cœur (Python) :** Gère la logique de la chaîne, la validation des blocs et la mempool.

**La Couche P2P :** Gère les sockets pour connecter les nœuds entre eux.

**L'API Flask :** Fait le pont entre la blockchain et l'interface utilisateur.

### 📦 Installation et Lancement (Docker)
La méthode recommandée est d'utiliser Docker Compose pour simuler un réseau de 3 nœuds sur votre machine.

1. Prérequis

    Docker et Docker Compose installés. 
    Python 3.13 (si vous voulez lancer les tests localement).

2. Démarrage du réseau

*Construire et lancer les 3 nœuds (System, Client 1, Client 2)*

```docker-compose up --build ```
3. Accès aux interfaces
Chaque nœud expose son propre portefeuille web sur un port différent :

* Nœud Système : http://localhost:8080

* Client 1 : http://localhost:8081

* Client 2 : http://localhost:8082

### 🧪 Tests Unitaires
Les tests sont automatiquement lancés lors du docker build. Pour les lancer manuellement dans votre environnement virtuel :

``` pytest tests/ ```

**Ce qui est testé :**

* Génération de clés et d'adresses.

* Intégrité des signatures DER (Compatibilité Python/JS).

* Validation du Proof of Work (difficulté des 0).

* Synchronisation des blocs entre deux instances de blockchain.

### 📝 Guide d'utilisation
1. **Créer un Wallet :** Cliquez sur "Créer wallet" sur le Client 1 et le Client 2.
2. **Transaction :** Copiez l'adresse du Client 2, collez-la dans l'interface du Client 1, saisissez un montant et envoyez.
3. **Propagation :** La transaction apparaît instantanément dans la Mempool des deux clients.
4. **Minage :** Cliquez sur "Miner bloc". Un nouveau bloc est généré, validé par le réseau et ajouté à la Blockchain visible en bas de page.

### ⚠️ Sécurité et Limitations
* **Pas de Persistence :** La chaîne est stockée en mémoire (RAM). Redémarrer Docker réinitialise la blockchain.

* **Double Dépense :** Le système de balance est simplifié et ne vérifie pas encore les UTXO (Unspent Transaction Outputs) en temps réel avant l'ajout à la mempool.
