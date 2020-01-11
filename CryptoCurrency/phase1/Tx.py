import random
import DS

def serialNumberGen(b):
#b for bitsize
	serial = random.randrange(2**(b-1),(2**(b))-1)
	return serial

def gen_random_tx(q,p,g):
	lines = [""]*7
	lines[0]="***Bitcoin transaction"
	lines[1]="Serial number:"+str(serialNumberGen(128))
	a,b=DS.KeyGen(q,p,g)
	lines[2]="Payer public key (beta): "+str(b)
	a2,b2=DS.KeyGen(q,p,g)
	lines[3]="Payee public key (beta):"+str(b2)
	amount=random.randrange(0,100000)
	lines[4]="Amount:"+str(amount)
	sign = '\n'.join(lines[0:5])+'\n'
	s,r=DS.SignGen(sign.encode('utf-8'),q,p,g,a)
	lines[5]="Signature (s): "+str(s)
	lines[6]="Signature (r): "+str(r)
	ret=""

	for i in range(0,7):
		#print(lines[i])
		ret+=lines[i]+"\n"
	return ret



"""
Hakan Bugra Erentug - Nidanur Günay
CS411 Project Phase I
05/12/19
Erkay Savaş - Fall 2019
"""
