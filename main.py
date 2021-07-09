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

# Creating wallets :
wallet1 = wallet.Wallet()
wallet2 = wallet.Wallet()
wallet3 = wallet.Wallet()
wallet1.save()
wallet2.save()
wallet3.save()

blockchain.add_block()


####
