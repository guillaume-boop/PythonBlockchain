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

        blockchain.add_transaction("Guigz", "Yoyo", 10)

        self.assertEqual(len(blockchain.pending_transactions), 1)
        self.assertEqual(blockchain.pending_transactions[0].sender, "Guigz")
        self.assertEqual(blockchain.pending_transactions[0].recipient, "Yoyo")
        self.assertEqual(blockchain.pending_transactions[0].amount, 10)

    # Tests to block transactions if argmuent are empty and amount
    def test_add_transaction_empty_sender(self):  
        blockchain = Blockchain()

        blockchain.create_genesis_block()

        with self.assertRaises(ValueError):
            blockchain.add_transaction("", "Yoyo", 10)


    def test_add_transaction_empty_receiver(self):  
        blockchain = Blockchain()

        blockchain.create_genesis_block()

        with self.assertRaises(ValueError):
            blockchain.add_transaction("Guigz", "", 10)


    def test_add_transaction_empty_amount(self):  
        
        blockchain = Blockchain()
        
        blockchain.create_genesis_block()

        with self.assertRaises(ValueError):
            blockchain.add_transaction("Guigz", "Yoyo", 0)

    # Test mining a block
    def test_mine_block(self):
        
        blockchain = Blockchain()
        blockchain.chain = []
        blockchain.create_genesis_block()


        blockchain.add_transaction("Guigz", "Yoyo", 10)
        blockchain.add_transaction("Yoyo", "Guigz", 5)

        block_mined = blockchain.mine_pending_transactions()

        self.assertTrue(block_mined)
        self.assertEqual(len(blockchain.chain), 2)
        self.assertEqual(blockchain.chain[1].index, 1)
        self.assertEqual(len(blockchain.chain[1].transactions), 2)


    def test_mining_without_transactions(self):
        blockchain = Blockchain()
            
        if not blockchain.chain:
            blockchain.create_genesis_block()

        block_mined = blockchain.mine_pending_transactions()

        self.assertFalse(block_mined)
        self.assertEqual(len(blockchain.chain), 1)  


if __name__ == "__main__":
    unittest.main()