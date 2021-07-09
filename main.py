from classes import chain, wallet, block
from settings import settings
from os import listdir
from os.path import isfile, join
import sys

# Increasing the recursion limit from 1000 to 1000000 to avoid problems with the hash generation
sys.setrecursionlimit(10**6)

blockchain = chain.Chain()

# Loading the blocs already existing in 'content/blocs' to the chain

blocks_to_load = [f for f in listdir(settings.PATH_TO_BLOCS) if isfile(join(
    settings.PATH_TO_BLOCS, f))]
blocks_loaded = []
for f in blocks_to_load:
    hash, extension = str(f).split('.')
    b = block.Block.load(hash)
    blockchain.blocs[hash] = b
last_block_timestamp = 0
for hash, block in blockchain.blocs.items():
    if block.timestamp > last_block_timestamp:
        last_block_timestamp = block.timestamp
        blockchain.last_block_hash = block.hash

# Creating wallet and demonstration of the methods:

wallet1 = wallet.Wallet()

print("Let's create a wallet and see its content: ")
wallet1.to_string()

print("Let's add 500 tokens: ")
wallet1.add_balance(500)
wallet1.to_string()

print("Let's remove 400 tokens: ")
wallet1.sub_balance(400)
wallet1.to_string()

print("With a maximum token number of 10 000, let's see what happens if we add 1 000 000 "
      "tokens:")
wallet1.add_balance(1000000)

print("Let's save and load the same wallet:")
wallet1.save()
wallet1_bis = wallet.Wallet.load(wallet1.unique_id)
wallet1_bis.to_string()


# Creating a block and demonstration of the methods:
print("Now, let's create a blockchain and our first block:")
blockchain = chain.Chain()
blockchain.add_block()
current_block = blockchain.get_block(blockchain.last_block_hash)
current_block.to_string()
print("Test case: the base_hash verify the hash:")
print(current_block.check_hash())


wallet2 = wallet.Wallet()
wallet2.save()
print("Let's make some transactions:")
print("Test case : the transmitter does not exist:")
blockchain.add_transaction("FakeWalletID", wallet2.unique_id, 50)
print("Test case : the receiver does not exist:")
blockchain.add_transaction(wallet1.unique_id, "anotherFakeWalletId", 50)
print("Test case : the transmitter does not have enough token:")
blockchain.add_transaction(wallet1.unique_id, wallet2.unique_id, 5000)

print("Real case : wallet1 transmit 100 tokens to wallet3:")
blockchain.add_transaction(wallet1.unique_id, wallet2.unique_id, 48.75)
print("Let's see what is inside the two concerned wallets:")
wallet1 = wallet.Wallet.load(wallet1.unique_id)
wallet1.to_string()
wallet2 = wallet.Wallet.load(wallet2.unique_id)
wallet2.to_string()
print("Let's see if our transaction has been added to the list in our current block:")
current_block.to_string()

print("Let's save our block and load it again, then, we'll check its size in bytes")
current_block.save()
current_block_bis = block.Block.load(current_block.hash)
current_block_bis.to_string()
size = current_block.get_weight()
print("File size of the block = " + str(size) + " bytes")

print("Even if we have less than 256000 bytes, let's create a new block and make additional "
      "transactions:")
wallet3 = wallet.Wallet()
wallet3.save()
blockchain.add_block()
blockchain.add_transaction(wallet1.unique_id, wallet3.unique_id, 24)
blockchain.add_transaction(wallet2.unique_id, wallet3.unique_id, 50)
blockchain.add_transaction(wallet1.unique_id, wallet2.unique_id, 45)
blockchain.add_transaction(wallet2.unique_id, wallet1.unique_id, 10)
blockchain.add_transaction(wallet3.unique_id, wallet2.unique_id, 43.50)
blockchain.add_transaction(wallet3.unique_id, wallet2.unique_id, 49.50)
blockchain.add_transaction(wallet2.unique_id, wallet1.unique_id, 60)

current_block = blockchain.get_block(blockchain.last_block_hash)
print("Let's see some transactions in details:")
print("1st transaction:")
print(current_block.get_transaction(0))
print("2nd transaction:")
print(current_block.get_transaction(1))
print("5th transaction:")
print(current_block.get_transaction(4))

print("The corresponding wallets have changed according to the transactions:")
wallet1 = wallet.Wallet.load(wallet1.unique_id)
wallet2 = wallet.Wallet.load(wallet2.unique_id)
wallet3 = wallet.Wallet.load(wallet3.unique_id)
wallet1.to_string()
wallet2.to_string()
wallet3.to_string()

print("We can get the number of transactions we made in our blockchain:")
print(blockchain.get_last_transaction_number())
print("And we can find the bloc in which each transaction has been made:")
print("Let's check if the 1st transaction has been made in the first block (id=0):")
searched_block = blockchain.find_transaction(1)
print("block id: " + str(searched_block.unique_id))
print("Let's check if the 4th transaction has been made in the first block (id=1):")
searched_block = blockchain.find_transaction(4)
print("block id: " + str(searched_block.unique_id))

print("Finally, let's see what's in our blockchain:")
blockchain.to_string("blockchain")