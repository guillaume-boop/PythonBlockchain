import json
import os
from time import time
from block import Block
from transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 2
        self.load_from_file()

    def create_genesis_block(self):
        genesis_block = Block(index=0, transactions=[], timestamp=time(), previous_hash="0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]
    
    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        self.pending_transactions.append(transaction)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    def mine_pending_transactions(self):
        if not self.pending_transactions:
            print("Aucune transaction à miner.")
            return False

        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.pending_transactions,
            timestamp=time(),
            previous_hash=last_block.hash
        )

        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []
        print(f"Bloc #{new_block.index} miné avec succès : {new_block.hash}")
        return True


    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Recalcul du hash du bloc courant
            if current.hash != current.compute_hash():
                print(f"Bloc #{current.index} : hash invalide.")
                return False

            # Vérifie le lien avec le bloc précédent
            if current.previous_hash != previous.hash:
                print(f"Bloc #{current.index} : lien avec le bloc précédent invalide.")
                return False

        return True
    

    def save_to_file(self, filename="blockchain.json"):
        data = []
        for block in self.chain:
            data.append({
                "index": block.index,
                "timestamp": block.timestamp,
                "transactions": [tx.to_dict() for tx in block.transactions],
                "previous_hash": block.previous_hash,
                "nonce": block.nonce,
                "hash": block.hash
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename="blockchain.json"):
        if not os.path.exists(filename):
            self.create_genesis_block()
            return

        with open(filename, "r") as f:
            data = json.load(f)

        self.chain = []
        for b in data:
            transactions = [Transaction(**tx) for tx in b["transactions"]]
            block = Block(
                index=b["index"],
                transactions=transactions,
                timestamp=b["timestamp"],
                previous_hash=b["previous_hash"],
                nonce=b["nonce"]
            )
            block.hash = b["hash"]
            self.chain.append(block)

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.validate_chain(new_chain):
            self.chain = new_chain
            print("✅ Chaîne remplacée par une version plus longue.")
            return True
        else:
            print("❌ Chaîne reçue invalide ou plus courte.")
            return False


    def validate_chain(self, chain):
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]

            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def load_external_chain(self, filename):
        if not os.path.exists(filename):
            print("❌ Fichier de chaîne externe introuvable.")
            return None

        with open(filename, "r") as f:
            data = json.load(f)

        external_chain = []
        for b in data:
            transactions = [Transaction(**tx) for tx in b["transactions"]]
            block = Block(
                index=b["index"],
                transactions=transactions,
                timestamp=b["timestamp"],
                previous_hash=b["previous_hash"],
                nonce=b["nonce"]
            )
            block.hash = b["hash"]
            external_chain.append(block)

        return external_chain
