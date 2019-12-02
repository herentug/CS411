# use "pip install pyprimes" if pyprimes is not installed
# use "pip install pycryptodome" if pycryptodome is not installed
import random
import pyprimes
import warnings
from Crypto.Hash import SHA3_256
from Crypto.Hash import SHAKE128

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
        chck = pyprimes.is_prime(p)
    warnings.simplefilter('default')    
    return p

def large_DL_Prime(q, bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)
        p = k*q+1
        chck = pyprimes.is_prime(p)
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

# Signature generation
def Sig_Gen(message, a, k, q, p, g):
    shake = SHAKE128.new(message)
    h = int.from_bytes(shake.read(q.bit_length()//8), byteorder='big')
    r = pow(g, k, p)%q
    s = (modinv(k, q)*(h+a*r))%q
    return r, s

# Signature verification
def Sig_Ver(message, r, s, beta, q, p, g):
    shake = SHAKE128.new(message)
    h = int.from_bytes(shake.read(q.bit_length()//8), byteorder='big')
    u1 = (modinv(s, q)*h)%q
    u2 = (modinv(s, q)*r)%q
    v1 = (pow(g, u1, p)*pow(beta, u2, p)%p)%q

    if v1 == r:
        return True
    else:
        return False

# Test
print("Testing the DSA signature generation and verification")
# Generate domain parameters (q, p, g)
q, p, g = Param_Generator(160, 1024)
print("q =", q)
print("p =", p)
print("g =", g)

# Generate private-public key pairs for a user
a, beta = Key_Gen(q, p, g)
print("secret key (a):", a)
print("public key (beta):", beta)

message = b'Hello World!'
k = random.randint(0, q-1)
r, s = Sig_Gen(message, a, k, q, p, g)

if Sig_Ver(message, r, s, beta, q, p, g):
    print("signature verifies:) ")
else:
    print("invalid signature:( ")

# Question 5 starts here

q = 897434149680309024926610536586679400252190817513

p = 97223004199266313523049166053330029092380541300786138924873181088471438705453794046370914345592432368059271294544102722787957310837797304650943069820520287549826630230617625792526214799206486444554607275157031742808122667064876655138748567945051878459968434840972135354745893868660267009794876094057307360271

g = 4621497210057935612371988511711932510361318115609980978853236984314561739819039313271820105098638480214293876477070872723831493769268422441714876014396954567136665583461293138792502100498181714605761615088670098808016625617309860858682957197265294737395362167975930097648958972424479880194787709852371142579

public_key_beta = 45720223092558820344769930028614803638859051907129501277880999062740852114889610377894039520973053847174144955552627174266061939323577184681728281156812736603122999262209953001238229439108117677423857541271841004309469066208083385254271589636542160767902921803860270699359911081346969522186114311390226677995

message1 = b"He who laugh last didn't get the joke"
r1 = 867552604169477346883674422144796797059303863627
s1 = 243861349833858115605937030382497401412336608822

message2 = b"Ask me no questions, and I'll tell you no lies"
r2 = 686145019080375810998084468514665120375929537329
s2 = 774583422188330317252601038183072854135396118762

# k2 = 2k1 mod q

# alfa = (si * hj - sj * hi * x) * modinv((sj * ri * x - si * rj), q)
# above equation is taken from the last slide of the ch10_handout

h1 = pow(g, s1, p)  # taken from KeyGen function
h2 = pow(g, s2, p)
first_part_of_the_equation = (s1 * h2) - (s2*h1*2)
second_part_of_the_equation = modinv((s2 * r1 * 2 - s1 * r2),q)


alfa = (first_part_of_the_equation * second_part_of_the_equation) % q
print("Alfa is " + str(alfa))

if Sig_Ver(message1, r1, s1, public_key_beta, q, p, g): # checking if signature verifies for message1
    print("signature verifies:) ")
else:
    print("invalid signature:( ")

if Sig_Ver(message2, r2, s2, public_key_beta, q, p, g): # checking if signature verifies for message2
    print("signature verifies:) ")
else:
    print("invalid signature:( ")
