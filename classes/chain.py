import hashlib
from classes import block, wallet
import string
import random
from random import randint, random, choice


class Chain:
    def __init__(self):
        self.blocs = {}
        self.last_transaction_number = 0
        self.last_block_hash = None

    def generate_hash(self):
        generated_hash = ""
        while not self.verify_hash(generated_hash):
            string_sequence = ""
            for i in range(randint(1, 100)):
                string_sequence += choice(string.ascii_letters)
            generated_hash = hashlib.sha256(string_sequence.encode()).hexdigest()
        return string_sequence, generated_hash

    def verify_hash(self, hash_to_check):
        if ("hash", hash_to_check) not in self.blocs.items() and hash_to_check.startswith("0000"):
            return True

    def add_block(self):
        """Create a new block and assign the last block created as parent. generate_hash() use
        the method verify_hash() to check is no block with the found hash already exists. Once
        created, the new block is linked to the last block created in the chain or is assigned as
        the origin block (parent_hash = "00"), then added to the chain and saved in Json format in
        content/blocs"""
        base_hash, new_hash = self.generate_hash()
        if not self.blocs:
            parent_hash = "00"
        else:
            parent_bloc = self.get_block(self.last_block_hash)
            parent_hash = parent_bloc.hash
        new_block = block.Block(base_hash, new_hash, parent_hash)
        self.blocs[new_hash] = new_block
        self.last_block_hash = new_hash
        new_block.save()

    def get_block(self, hash_searched):
        for hash, bloc in self.blocs.items():
            if hash == hash_searched:
                return bloc

    def add_transaction(self, transmitter, receiver, amount):

        b = self.get_block(self.last_block_hash)
        file_size = b.get_weight()
        if file_size >= 256000:
            self.add_block()
            b = self.get_block(self.last_block_hash)
        t = wallet.Wallet.load(transmitter)
        r = wallet.Wallet.load(receiver)
        if t is None:
            return print("Transaction aborted : wallet n°" + str(transmitter) + "has not been "
                                                                                "found")
        if r is None:
            return print("Transaction aborted : wallet n°" + str(receiver) + " has not been found")
        if t.balance - amount < 0:
            return print("Transaction aborted : insufficient balance on transmitter wallet")
        t.sub_balance(amount)
        t_history = "%d has been credited to %s" % (amount, str(receiver))
        t.history.append(t_history)
        t.save()
        r.add_balance(amount)
        r_history = "%d has been credited by %s" % (amount, str(transmitter))
        r.history.append(r_history)
        r.save()
        b.add_transaction(str(transmitter), str(receiver), amount)
        b.save()
        self.last_transaction_number += 1

    def find_transaction(self, transaction_number):
        if transaction_number not in range(1, self.last_transaction_number):
            return print("This transaction does not exist")
        i = 1
        for hash, block in self.blocs.items():
            for j in range(len(block.transactions)):
                if j+i == transaction_number:
                    return block
            i += len(block.transactions)

    def get_last_transaction_number(self):
        return self.last_transaction_number

