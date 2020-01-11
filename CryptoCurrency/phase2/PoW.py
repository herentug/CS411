import math
import random
import string
import warnings
import sympy
import DS       # This is the file from Phase I
import Tx       # This is the first file you have to submit in the second phase 
     # This is the second file you have to submit in the second phase 
import os.path
import sys
import DS
from Crypto.Hash import SHA3_256

def hash(message):
	h_obj = SHA3_256.new()
	h_obj.update(message)
	h = h_obj.digest()
	return h


def CheckPow(p, q, g, digit, TxCnt, filename):	
	f = open(filename, "r")
	tx_block = f.readlines()
	f.close()
	tree=[""]*128
	for i in range(0,64):
    		tree[i+64] = hash(("".join(tx_block[i*7: i*7+7]).encode("utf-8")))
	for i in range(63,0,-1):
    		tree[i] = hash(tree[(2*i)]+tree[(2*i)+1])
	H_r=tree[1]
	nonce=int(tx_block[-1][7:-1])
	h_obj = SHA3_256.new()
	h_obj.update((H_r + (str(nonce)+'\n').encode('UTF-8')))
	h = h_obj.hexdigest()

	digest = h
	return digest


def PoW(l,q,p,g, TxCnt, filename):
	f = open(filename, "r")
	tx_block = f.readlines()
	f.close()
	tree=[""]*128
	for i in range(0,64):
    		tree[i+64] = hash(("".join(tx_block[i*7: i*7+7]).encode("utf-8")))
	for i in range(63,0,-1):
    		tree[i] = hash(tree[(2*i)]+tree[(2*i)+1])
	H_r=tree[1]

	nonce=random.randrange(2**31,(2**32)-1)
	h_obj = SHA3_256.new()
	h_obj.update((H_r + (str(nonce)+'\n').encode('UTF-8')))
	h = h_obj.hexdigest()
	digest = h
	zero="0"*l	#000 
	while(digest[:l]!=zero):
		nonce=random.randrange(2**31,(2**32)-1)
		h_obj = SHA3_256.new()
		h_obj.update((H_r + (str(nonce)+'\n').encode('UTF-8')))
		digest = h_obj.hexdigest()
	tx_block.append("Nonce: "+str(nonce)+'\n')
	return "".join(tx_block[:])
	



# Hakan Buğra Erentuğ - Nidanur Günay
# 23637 - 24231
# Phase 2 - 13/12/19
