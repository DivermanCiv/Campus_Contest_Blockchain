import json
import hashlib
import os
import time
from pathlib import Path
from settings import settings


class Block:
    def __init__(self, base_hash, hash, parent_hash, transactions=None, timestamp=None):
        self.base_hash = base_hash
        self.hash = hash
        self.parent_hash = parent_hash
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = transactions
        if timestamp is None:
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp

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
        path = Path(settings.PATH_TO_BLOCS + "\\" + self.hash + ".json")
        if not os.path.exists(path):
            self.save()
        weight = int(os.path.getsize(path))
        return weight

    def save(self):
        data = {
            "base_hash": self.base_hash,
            "hash": self.hash,
            "parent_hash": self.parent_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp
        }
        file_name = self.hash + ".json"
        path = Path(settings.PATH_TO_BLOCS)
        with open(os.path.join(path, file_name), "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def load(hash):
        path = Path(settings.PATH_TO_BLOCS)
        file_name = str(hash) + ".json"
        try:
            with open(os.path.join(path, file_name), "r") as read_file:
                data = json.load(read_file)
                block = Block(data["base_hash"], data["hash"], data["parent_hash"],
                              data["transactions"], data["timestamp"])
            return block
        except FileNotFoundError:
            return None
