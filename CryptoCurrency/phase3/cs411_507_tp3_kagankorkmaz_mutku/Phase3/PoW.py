from Crypto.Hash import SHA3_256
import os
import random
def MerkleTree(filename, TxCnt):
    
    f = open(filename, 'r')
    tx_block = f.readlines()
    f.close()
    block_count = len(tx_block)//7
    merkle1 = [0]*block_count
    
    for i in range(0, block_count):
        tx = "".join(tx_block[i*7: i*7+7])
        hash = SHA3_256.new(tx.encode('utf-8'))
        #merkle1[i] = hash
        merkle1[i] = hash.digest()
        #print(merkle1[i])

    while(block_count != 1):
        block_count = block_count // 2
        for i in range(0, block_count):
            hash = SHA3_256.new(merkle1[2*i] + merkle1[(2*i)+1])
            #merkle1[i] = hash
            merkle1[i] = hash.digest()
    #print(merkle1[0])
    return merkle1[0]

'''
x = MerkleTree('block_sample.txt', 64)
print(x)
print(type(x))



print("###########################")
'''
def CheckPow(p, q, g, PoWLen, TxCnt, filename):

    f = open(filename, 'r')
    lines = f.readlines()
    nonce = lines[-1][7:]
    f.close()
    
    Hr = MerkleTree(filename, TxCnt)
    #print("type: ", type(Hr))
    #print(nonce)
    #print(Hr)

    #nonce = nonce.encode('utf-8')
    #Hr = Hr.encode('utf-8')
    
    hash = SHA3_256.new((Hr + nonce.encode('utf-8')))

    PoW = hash.hexdigest()

    s = ''
    for i in range(0, PoWLen):
        s = s + '0'

    if PoW[0:PoWLen] == s:
        return PoW

    else:
        return ''

    

def PoW(PoWLen, q, p, g, TxCnt, filename):
    f = open(filename, 'r')
    lines = f.readlines()
   
    f.close()
    
    Hr = MerkleTree(filename, TxCnt)
    #hash = SHA3_256.new((Hr + nonce).encode('utf-8'))

    #PoW = hash.hexdigest()

    s = ''
    for k in range(0, PoWLen):
        s = s + '0'
    #i = 0
    while(1):
        nonce = str(random.randint(0, 2**128)) + '\n'
        hash = SHA3_256.new(Hr + nonce.encode('utf-8'))
        PoW = hash.hexdigest()
        if PoW[0:PoWLen] == s:
            #print("nonce: ", nonce, 'PoW: ', PoW)
            #print(PoW)
            break
            
    lines = "".join(lines) 
    lines = lines + 'Nonce: ' + str(nonce)
    return lines


