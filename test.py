from block import Block
from transaction import Transaction
from blockchain import Blockchain
from time import time
import unittest
import os

class TestBlockchain(unittest.TestCase):
    
    # Test the genesis block creation
    def test_genesis_block(self):

        blockchain = Blockchain()
        blockchain.chain = []
        blockchain.create_genesis_block()

        self.assertEqual(len(blockchain.chain), 1)
        self.assertEqual(blockchain.chain[0].index, 0)
        self.assertEqual(blockchain.chain[0].previous_hash, "0")
        

    # Test adding a new block to the blockchain
    def test_add_transaction(self):

        blockchain = Blockchain()

        blockchain.create_genesis_block()

        blockchain.add_transaction("Alice", "Bob", 10)

        self.assertEqual(len(blockchain.pending_transactions), 1)
        self.assertEqual(blockchain.pending_transactions[0].sender, "Alice")
        self.assertEqual(blockchain.pending_transactions[0].recipient, "Bob")
        self.assertEqual(blockchain.pending_transactions[0].amount, 10)

        
    
if __name__ == "__main__":
    unittest.main()