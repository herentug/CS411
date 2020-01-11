import random
import pyprimes
import warnings
from Crypto.Hash import SHAKE128
from Crypto.Hash import SHA3_256
import string
import sympy

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    if a < 0:
        a = a+m
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m
    
def random_prime(bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        p = random.randrange(2**(bitsize-1), 2**bitsize-1)
        chck = sympy.isprime(p)
    warnings.simplefilter('default')    
    return p

def large_DL_Prime(q, bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)
        p = k*q+1
        chck = sympy.isprime(p) and p.bit_length() == 2048
    warnings.simplefilter('default')    
    return p

def Param_Generator(qsize, psize):
    q = random_prime(qsize)
    p = large_DL_Prime(q, psize-qsize)
    tmp = (p-1)//q
    g = 1
    while g == 1:
        alpha = random.randrange(1, p)
        g = pow(alpha, tmp, p)
    return q, p, g

def modinv(a, m):
    if a < 0:
        a = a+m
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


def KeyGen (q, p, g):
    a=random.randrange(0,q-1) # a will be picked by the user. 
    b = pow(g, a, p)
    return a,b

def random_string(stringLength=10):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))

def SignGen(message,q,p,g,a):
    h_obj = SHA3_256.new()
    h_obj.update(message)
    h = h_obj.hexdigest()
    h=int(h, 16)

    k = random.randrange(1, q - 2)
    r = (pow(g, k, p)) % q
    s = ((a * r) - (k * h)) % q
    return s,r

def SignVer(message,s,r,q,p,g,beta):

    h_obj = SHA3_256.new()
    h_obj.update(message)
    h = h_obj.hexdigest()
    h=int(h, 16)

    v = modinv(h, q)
    z1 = s * v % q
    z2 = r * v % q
    inv_g=modinv(g,p)
    u = (pow(inv_g,z1,p)*pow(beta,z2,p)%p)%q

    if (u == r):
        return 0
    else:
        return 1


def GenerateOrRead(filename):
	try:
		f = open(filename, "r")
		q = int(f.readline())
		p = int(f.readline())
		g = int(f.readline())
	except:
		q, p, g = Param_Generator(224,2048)
		

	return q,p,g



"""
Hakan Bugra Erentug - Nidanur Günay
CS411 Project Phase II
05/12/19
Erkay Savaş - Fall 2019
"""
