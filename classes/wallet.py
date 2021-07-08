import uuid, json, os
from pathlib import Path
from os import listdir
from os.path import isfile, join


class Wallet:
    def __init__(self, unique_id=None, balance=100, history= None):
        if unique_id is None:
            self.unique_id = self.generate_unique_id()
        else:
            self.unique_id = unique_id
        self.balance = balance
        if history is None:
            self.history = []
        else:
            self.history = history

    def generate_unique_id(self):
        unique_id = uuid.uuid4()
        path = Path('content/wallets')
        wallets = [f for f in listdir(path) if isfile(join(path, f))]
        walletsId = []
        for f in wallets:
            otherId, extension = str(f).split('.')
            walletsId.append(otherId)
        for otherId in walletsId:
            if str(unique_id) == otherId:
                self.generate_unique_id()
        return unique_id

    def add_balance(self, montant):
        self.balance += montant

    def sub_balance(self, montant):
        self.balance -= montant

    def send(self):
        pass

    def save(self):
        data = {
            "unique_id": str(self.unique_id),
            "balance": self.balance,
            "history": self.history
        }
        fileName = str(self.unique_id)+".json"
        path = Path('content/wallets')
        with open(os.path.join(path, fileName), "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def load(unique_id):
        path = Path('content/wallets')
        fileName = str(unique_id) + ".json"
        with open(os.path.join(path, fileName), "r") as read_file:
            data = json.load(read_file)
        wallet = Wallet(data["unique_id"], data["balance"], data["history"])
        return wallet

