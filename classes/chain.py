import hashlib
from classes import block, wallet
import string
import random
from random import randint, random, choice


class Chain:
    def __init__(self):
        self.blocs = {}
        self.last_transaction_number = None
        self.last_block_hash = None

    def generate_hash(self):
        string_sequence = ""
        generated_hash = ""
        while not self.verify_hash(generated_hash):
            for i in range(randint(1, 100)):
                string_sequence += choice(string.ascii_letters)
            generated_hash = hashlib.sha256(string_sequence.encode()).hexdigest()
        return string_sequence, generated_hash

    def verify_hash(self, hash_to_check):
        if ("hash", hash_to_check) not in self.blocs.items() and hash_to_check.startswith("0000"):
            return True

    def add_block(self):
        base_hash, new_hash = self.generate_hash()

        if self.get_block(new_hash) is None:
            parent_hash = 00
            new_block = block.Block(base_hash, new_hash, parent_hash)

    def get_block(self, hash_searched):
        for hash, bloc in self.blocs.items():
            if hash == hash_searched:
                return bloc
    # def add_transaction(self):
    #
    # def find_transaction(self):
    #
    # def get_last_transaction_number(self):

