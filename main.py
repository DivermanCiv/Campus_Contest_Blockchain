import os
from pathlib import Path
from classes import chain, wallet, block
from os import listdir
from os.path import isfile, join
import sys

# Tests
# myChain = chain.Chain()
# wallet1 = wallet.Wallet()
#
# wallet1.save()
#
# wallet2 = wallet.Wallet.load(wallet1.unique_id)
#
# print(wallet2.unique_id + " - " + str(wallet2.balance))
# wallet2.add_balance(500)
# wallet2.save()
# wallet3 = wallet.Wallet.load(wallet2.unique_id)
# print(wallet3.unique_id + " - " + str(wallet2.balance))

chain = chain.Chain()
chain.blocs["truc"]="muche"
print(chain.get_block("truc"))
print(chain.get_block("autre"))
####