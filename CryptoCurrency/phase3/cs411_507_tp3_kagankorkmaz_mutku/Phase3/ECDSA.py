import math
import random
import string
import warnings
import os.path
import sys
# These are the modules needed for elliptic curve cryptography
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256

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

##############################

def KeyGen(E):
    order = E.order

    sA = random.randint(2, order-2)
    p = E.generator # P: base (generator point) P
    QA = sA*p
    return sA, QA

def SignGen(message, E, sA):
    n = E.order
    p = E.generator
    
    hash = SHA3_256.new(message)
    h = int.from_bytes(hash.digest(), byteorder='big')
    k = random.randint(1, n-1)
    R = k*p
    r = R.x % n
    s = (modinv(k, n) * (h + sA*r)) % n

    return s,r

def SignVer(message, s, r, E, QA):
   
    n = E.order
    p = E.generator

    hash = SHA3_256.new(message)
    h = int.from_bytes(hash.digest(), byteorder='big')

    s_1 = modinv(s,n)
    u1 = (s_1 * h) % n
    u2 = (s_1 * r) % n

    p = p*u1
    QA = QA*u2

    slope = (p.y - QA.y) / (p.x - QA.x)
    
    v = ((slope**2) - p.x - QA.x ) % n

    r = r%n

    if(v == r):
        return 0
    else:
        return 0
    
    

