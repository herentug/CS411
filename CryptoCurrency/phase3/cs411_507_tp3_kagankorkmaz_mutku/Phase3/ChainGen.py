import math
import random
import string
import warnings
import os.path
import sys
# These are the modules needed for elliptic curve cryptography
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256
  

#9 is the length of 1 transaction
def MerkleTree(tx_block, TxCnt):
    
    #f = open(filename, 'r')
    #tx_block = f.readlines()
    #f.close()
    block_count = len(tx_block)//9
    merkle1 = [0]*block_count
    
    for i in range(0, block_count):
        tx = "".join(tx_block[i*9: i*9+9])
        hash = SHA3_256.new(tx.encode('utf-8'))
        
        merkle1[i] = hash.digest()
       

    while(block_count != 1):
        block_count = block_count // 2
        for i in range(0, block_count):
            hash = SHA3_256.new(merkle1[2*i] + merkle1[(2*i)+1])
            
            merkle1[i] = hash.digest()
    
    return merkle1[0]


def AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock):
    s = ''
    for k in range(0, PoWLen):
        s = s + '0'
    
    if PrevBlock == '':  # first block in the chain.
        PrevPoW =  '00000000000000000000'
        PrevPoW_byte = PrevPoW.encode('utf-8')

        H_r = MerkleTree(block_candidate, TxCnt)
        
        while(1):
            Nonce = random.randint(0,2**128)
            hash = SHA3_256.new(H_r + PrevPoW_byte + Nonce.to_bytes((Nonce.bit_length()+7)//8, byteorder = 'big'))
            PoW = hash.hexdigest()
            if PoW[0:PoWLen] == s:
                break
        
        block_candidate = "".join(block_candidate)
        block_candidate = block_candidate + "Previous PoW: " + PrevPoW + "\n"
        block_candidate = block_candidate + "Nonce: " + str(Nonce) + "\n"

        return block_candidate, PrevPoW

    else:    
        # For the find PoW of the previous block
        
        Prev_H_r = MerkleTree(PrevBlock, TxCnt)
       
        PrevPrevPoW = PrevBlock[-2][14:-1]
        PrevPrevPoW_byte = PrevPrevPoW.encode('UTF-8')
       
        PrevNonce = int(PrevBlock[-1][7:-1])
       
        hash = SHA3_256.new(Prev_H_r + PrevPrevPoW_byte + PrevNonce.to_bytes((PrevNonce.bit_length()+7)//8, byteorder = 'big'))
        PrevPoW = hash.hexdigest()
        
        # For the block we are in
        H_r = MerkleTree(block_candidate, TxCnt)

        while(1):
            Nonce = random.randint(0,2**128)
            hash = SHA3_256.new(H_r + PrevPoW.encode('utf-8') + Nonce.to_bytes((Nonce.bit_length()+7)//8, byteorder = 'big'))
            PoW = hash.hexdigest()
            if PoW[0:PoWLen] == s:
                break

        block_candidate = "".join(block_candidate)
        block_candidate = block_candidate + "Previous PoW: " + PrevPoW + "\n"
        block_candidate = block_candidate + "Nonce: " + str(Nonce) + "\n"

        
        return block_candidate, PrevPoW
    
