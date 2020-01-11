import math
import random
import string
import warnings
import sympy

import Tx       # This is the first file you have to submit in the second phase 
     # This is the second file you have to submit in the second phase 
import os.path
import sys

from Crypto.Hash import SHA3_256

def hash(message):
	h_obj = SHA3_256.new()
	h_obj.update(message)
	h = h_obj.digest()
	return h

TxLen=9
def PoW(l, TxCnt, Block):

	hashTree = []
	for i in range(0,TxCnt):
		transaction = "".join(Block[i*TxLen:(i+1)*TxLen])
		hashTree.append(SHA3_256.new(transaction.encode('UTF-8')).digest())
	t = TxCnt
	j = 0
	while(t>1):
		for i in range(j,j+t,2):
			hashTree.append(SHA3_256.new(hashTree[i]+hashTree[i+1]).digest())
		j += t
		t = t>>1
	H_r = hashTree[2*TxCnt-2]


	PrevPoW = Block[-2][14:-1]
	

	nonce=random.randrange(2**31,(2**32)-1)
	digest = H_r + PrevPoW.encode('utf-8') + nonce.to_bytes((nonce.bit_length()+7)//8, byteorder = 'big')
	PoW = SHA3_256.new(digest).hexdigest()

	while(PoW[0:l]!=l*"0"):
		nonce=random.randrange(2**31,(2**32)-1)
		digest = H_r + PrevPoW.encode('utf-8') + nonce.to_bytes((nonce.bit_length()+7)//8, byteorder = 'big')
		PoW = SHA3_256.new(digest).hexdigest()

	return PoW,str(nonce)
	


def AddBlock2Chain(PoWLen,TxCnt, Block,Prev):
	
	if(Prev==""):
		PoW_="00000000000000000000"
		line='Previous PoW: '+ PoW_ +'\n'
		nonce="0"
		

		newBlock=Block
		newBlock.append(line)
		newBlock.append("Nonce: "+nonce)

		no2,nonce = PoW(PoWLen,TxCnt,newBlock)
		newBlock[-1]="Nonce: "+nonce+'\n'
	else:
		
		hashTree = []
		for i in range(0,TxCnt):
			transaction = "".join(Prev[i*TxLen:(i+1)*TxLen])
			hashTree.append(SHA3_256.new(transaction.encode('UTF-8')).digest())
		t = TxCnt
		j = 0
		while(t>1):
			for i in range(j,j+t,2):
				hashTree.append(SHA3_256.new(hashTree[i]+hashTree[i+1]).digest())
			j += t
			t = t>>1
		H_r = hashTree[2*TxCnt-2]
		PrevPoW = Prev[-2][14:-1]
		Prevnonce = int(Prev[-1][7:-1])
		digest = H_r + PrevPoW.encode('utf-8') + Prevnonce.to_bytes((Prevnonce.bit_length()+7)//8, byteorder = 'big')
		
		PoW_ = SHA3_256.new(digest).hexdigest()
		
		nonce="0"
		line='Previous PoW: '+ PoW_ +'\n'
		newBlock=Block
		newBlock.append(line)
		newBlock.append("Nonce: "+nonce)

		no2,nonce = PoW(PoWLen,TxCnt,newBlock)
		newBlock[-1]="Nonce: "+nonce+'\n'
	return "".join(newBlock[:]), PoW_



"""
Nidanur Günay- Hakan Buğra Erentuğ
Porject PhaseIII

"""
