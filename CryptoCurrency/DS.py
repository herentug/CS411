import random
import pyprimes
import warnings
from Crypto.Hash import SHAKE128
from Crypto.Hash import SHA3_256

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
    while chck == False:
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)
        p = k*q+1
        chck = pyprimes.isprime(p)
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


q,p,g=Param_Generator(224,2048)



a=int(input("Pick a random secret key between 0 - "+str(q-1)+":\n"))
b=pow(g,a,p);
print("Public Key: "+ str(b))

message=b'Erkay'
#m = int.from_bytes(message, byteorder='big')


h_obj = SHA3_256.new()
h_obj.update(message)
print (h_obj.hexdigest())
h=h_obj.hexdigest()

print("\nh: ",h)


k=random.randrange(1,q-2)
r=(pow(g,k,p))%q

i = int(h, 16)
s = ((a*r)-(k*i))%q

print("\nSignature (s,r): "+str(s) +" "+ str(r))


#print(m.to_bytes((m.bit_length()+7)//8, byteorder='big'))


v=modinv(i,q)
z1=s*v %q
z2 = r*v %q
u=(pow(modinv(g,p),z1,p)*pow(b,z2,p))%q

if(u==r):
	print("Accept")
else:
	print("Reject")


