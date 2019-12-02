# use "pip install pyprimes" if pyprimes is not installed
import random
import pyprimes
import warnings

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

# Generating private-public key pair
def Key_Gen(q, p, g):
    s = random.randint(1, q) # private key
    h = pow(g, s, p)         # public key
    return s, h

# Encryption
def Enc(message, h, q, p, g): # m is the message
    m = int.from_bytes(message, byteorder='big')
    k = random.randint(1, 2**16-1)
    r = pow(g, k, p)
    t = (pow(h, k, p)*m)%p
    return r, t

# Decryption
def Dec(r, t, s, q, p, g):
    m = (pow(r, q-s, p)*t)%p
    return m.to_bytes((m.bit_length()+7)//8, byteorder='big')
"""
# Test
print("Testing the ElGamal Encryption and Decryption")
# Generate domain parameters (q, p, g)
q, p, g = Param_Generator(160, 1024)
print("q =", q)
print("p =", p)
print("g =", g)

# Generate private-public key pairs for a user
s, h = Key_Gen(q, p, g)
print("secret key (s):", s)
print("public key (h):", h)

# Encrypt a random message
message = b'Hello World!'
r, t = Enc(message, h, q, p, g)
print("ciphertext (r, t):", r, t)
"""

q=1331165794223730998214479682055290809139803703979
p=157985265365233926063394088702502775477411699807450440916775405947257964574813502993749815770128973338289285516154109088043476314331444397215358170585840641049172791477662283893716386808139204949694492602287891654767148522867881937046157301612266431912023462991540765986938468014946969764702086638496649455657
g=135065956040029542891335614580458248416002250295204395146754036299690682917789289716583464736425816867965184913947179997468650756414729019331183463002574881956749358833871584578559474520218159551812002168419391427229522879948629379275361929622066470148375436287416532348407065836711249965189758444892419490190
h=65369531380434811091013169285144074654274264126019340876116721977646567453108441439476580614131141018711217039183159447339703498645723099709331310035001607050335740436825222938421053125935986024030566120585714682225125302549720107383365077208839310065478286374555114097276440333388769523316671044117487454589
r=3603216964442507357032842714265491356140106170126012271249273782498781062854993590551963255079610858746338241608699542316440867356686210833642816015952448905408390917797105408900214398591806869245572453652902222971116293353284737156497321871750301615013009395209713928847567903247743033867199791859981117263
t=42244680577489180150438247901105682607063917920969521526593784819134087337617171624434658483262821880559452723151685731248400300205495303414447593079691461437018769475479437685274446474785220966939670711206064076236087750024913718835564780638938635976122622009741305316868203434730711663863398065249173925645

for i in range(1, 2**16 - 1):
    possibleR = pow(g,i,p)
    if(r == possibleR):
        k = i

print("k = " + str(k))

temp = modinv(h**k, p)

m = (temp * t) % p
print(m.to_bytes((m.bit_length()+7)//8, byteorder='big'))






