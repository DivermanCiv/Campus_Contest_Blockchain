import json
import hashlib
import os
from pathlib import Path


class Block:
    def __init__(self, base_hash, hash, parent_hash):
        self.base_hash = base_hash
        self.hash = hash
        self.parent_hash = parent_hash
        self.transactions = []

    def check_hash(self):
        if self.hash == hashlib.sha256(self.base_hash.encode()).hexdigest():
            return True

    def add_transaction(self, transmitter, receiver, amount):
        self.transactions.append({"transmitter": transmitter, "receiver": receiver, "amount":
            amount})

    def get_transaction(self, index):
        return self.transactions[index]

    def get_weight(self):
        """check if block is registered. If not, save it, then returns the file size in bytes"""
        file_name = Path('content/blocs/') + self.hash + ".json"
        if not os.path.exists(file_name):
            self.save()
        weight = os.path.getsize(file_name)
        return weight

    def save(self):
        data = {
            "hash": self.hash,
            "parent_hash": self.parent_hash,
            "transactions": self.transactions
        }
        file_name = self.hash + ".json"
        path = Path('content/blocs')
        with open(os.path.join(path, file_name), "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def load(hash):
        path = Path('content/blocs')
        file_name = str(hash) + ".json"
        with open(os.path.join(path, file_name), "r") as read_file:
            data = json.load(read_file)
        block = Block(data["hash"], data["parent_hash"], data["transactions"])
        return block
