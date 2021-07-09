import uuid
import json
import os
from settings import settings
from pathlib import Path
from os import listdir
from os.path import isfile, join


class Wallet:
    def __init__(self, unique_id=None, balance=None, history= None):
        if unique_id is None:
            if settings.STARTING_BALANCE + settings.CURRENT_TOKEN_NUMBER > \
                    settings.MAX_TOKEN_NUMBER:
                raise Exception("Wallet creation aborted : it would result in too many token in "
                                "circulation")
            settings.CURRENT_TOKEN_NUMBER += settings.STARTING_BALANCE
            self.unique_id = self.generate_unique_id()
        else:
            self.unique_id = unique_id
        if balance is None:
            self.balance = settings.STARTING_BALANCE
        else:
            self.balance = balance
        if history is None:
            self.history = []
        else:
            self.history = history

    def generate_unique_id(self):
        unique_id = uuid.uuid4()
        path = Path(settings.PATH_TO_WALLETS)
        wallets = [f for f in listdir(path) if isfile(join(path, f))]
        wallets_id = []
        for f in wallets:
            other_id, extension = str(f).split('.')
            wallets_id.append(other_id)
        for otherId in wallets_id:
            if str(unique_id) == otherId:
                return self.generate_unique_id()
        return unique_id

    def add_balance(self, amount):
        if settings.CURRENT_TOKEN_NUMBER + amount > settings.MAX_TOKEN_NUMBER:
            return print("Transaction aborted : it would result in too many tokens in circulation")
        settings.CURRENT_TOKEN_NUMBER += amount
        self.balance += amount

    def sub_balance(self, amount):
        settings.CURRENT_TOKEN_NUMBER -= amount
        self.balance -= amount

    def send(self):
        pass

    def save(self):
        data = {
            "unique_id": str(self.unique_id),
            "balance": self.balance,
            "history": self.history
        }
        file_name = str(self.unique_id)+".json"
        path = Path(settings.PATH_TO_WALLETS)
        with open(os.path.join(path, file_name), "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def load(unique_id):
        path = Path(settings.PATH_TO_WALLETS)
        file_name = str(unique_id) + ".json"
        try:
            with open(os.path.join(path, file_name), "r") as read_file:
                data = json.load(read_file)
            wallet = Wallet(data["unique_id"], data["balance"], data["history"])
            return wallet
        except FileNotFoundError:
            return None

    def to_string(self):
        print("Wallet n°" + str(self.unique_id) + " : balance : " + str(self.balance) + ", "
        "history :" + str(self.history))
