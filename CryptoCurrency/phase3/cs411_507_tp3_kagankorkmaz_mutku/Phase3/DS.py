import random
import pyprimes
import warnings
import sympy
import os
from Crypto.Hash import SHA3_256
from Crypto.Hash import SHAKE128

import string
import random

def random_prime(bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        p = random.randrange(2**(bitsize-1), 2**bitsize-1)
        chck = pyprimes.isprime(p)
    warnings.simplefilter('default')    
    return p

def large_DL_Prime(q, bitsize):
    warnings.simplefilter('ignore')
    chck = False
    '''
    while chck == False:
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)
        #k = random.randrange(2**bitsize-1, 2**bitsize)
        p = k*q+1
        chck = sympy.isprime(p) 
     
    k = random.randrange(2**(bitsize-1), 2**bitsize-1)   
    p = k*q+1
    while p.bit_length() != 2048:
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)
        #k = random.randrange(2**bitsize-1, 2**bitsize)
        p = k*q+1
    '''
    while chck == False:
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)   
        p = k*q+1
        while p.bit_length() != 2048:
            k = random.randrange(2**(bitsize-1), 2**bitsize-1)
            #k = random.randrange(2**bitsize-1, 2**bitsize)
            p = k*q+1
            #print(p.bit_length())
        chck = sympy.isprime(p)
    
    warnings.simplefilter('default')    
    return p

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


############# FUNCTIONS WE NEED ####################

# CREATING RANDOM MESSAGE
def random_string(length): 
    return ''.join(random.choice(string.ascii_letters) for m in range(length))

# CRATING RANDOM TEST SIGNATURES (q,p,g)
def GenerateTestSignatures(qsize, psize):
    q = random_prime(qsize)
    p = large_DL_Prime(q, psize-qsize)
    tmp = (p-1)//q
    g = 1
    while g == 1:
        alpha = random.randrange(1, p)
        g = pow(alpha, tmp, p)
    return q, p, g

# TAKING PUBLIC PARAMETERS q,p,g IF THEY DOES NOT EXİST CREATING
def GenerateOrRead(file):
    if(os.path.exists(file)):
        fobj = open(file, 'r+')
        data = fobj.read()
        lines = data.split("\n")
            
        q = 0
        p = 0
        g = 0
        if len(lines[0]) == 0: #if the file exists but empty
            q, p, g = GenerateTestSignatures(224, 2048)
            fobj.writelines([str(q)+"\n",str(p)+"\n",str(g)+"\n"])
            fobj.close()
            return q, p, g
        else: # if the file exist
            q = int(lines[0])
            p = int(lines[1])
            g = int(lines[2])
            return q,p,g

        fobj.close()
    
    else:  #if the file does not exist
        fobj = open(file, 'w')
        q, p, g = GenerateTestSignatures(224, 2048)
        fobj.writelines([str(q)+"\n",str(p)+"\n",str(g)+"\n"])
        fobj.close()
        return q, p, g


# GENERATING KEYS FOR USERS alpha and beta
def KeyGen(q, p, g):
    alpha = random.randint(1, q) # private key
    beta = pow(g, alpha, p)      # public key
    return alpha, beta


# GENERATING SIGNAUTES FOR USERS
def SignGen(message, q, p, g, alpha):
    hash = SHA3_256.new(message)
    h = int.from_bytes(hash.digest(), byteorder='big')
    h = h % q
    k = random.randint(1, q-2)
    r = pow(g, k, p) % q
    s = ((alpha*r) - (k*h)) % q
    return s, r  

# VERIFYING SIGNATURES
def SignVer(message, s, r, q, p, g, beta):
    hash = SHA3_256.new(message)
    h = int.from_bytes(hash.digest(), byteorder='big')
    h = h % q
    v = modinv(h,q)
    z1 = (s*v) % q
    z2 = (r*v) % q
    
    u = ((pow(modinv(g,p), z1, p) * pow(beta, z2, p)) % p ) % q
    if u == r:
        return 0
    else:
        return -1


