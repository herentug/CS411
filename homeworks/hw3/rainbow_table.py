# Do not forget to install pycryptodome if not already installed
# pip install pycryptodome

import random
from Crypto.Hash import SHA256
from Crypto import Random
import json

def Reduction(x, Alphabet, length):
  pwd = ""
  t = x
  size = len(Alphabet)
  for j in range(0,length):
    pwd += Alphabet[t%size]
    t = t//size
  return pwd  

Alphabet = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z', 26:'.', 27:',', 28:'!', 29:'?'}
alpha_len = len(Alphabet)
pwd_len = 6
pwd_space = alpha_len**pwd_len 
t = 2**16
m = 2*(pwd_space//t)
# Example for computing one link in the chain; i.e., pwd(i+1) = R(H(pwd(i)))
print("This is how you compute one link in the hash chain")
pwd_i = "OO,XR." # a sample password
hash = SHA256.new(pwd_i.encode('utf-8')) # hash it
digest = int.from_bytes(hash.digest(), byteorder='big') # convert the hash into an integer
pwd_i1 = Reduction(digest%pwd_space, Alphabet, pwd_len) # Reduce it
print("pwd(i) --> pwd(i+1): ", pwd_i, "-->",pwd_i1)
 
# Read the rainbow table
f = open("rainbowtable.txt","r")
Rainbow_Table = json.loads(f.read())
f.close()

# Check one link in the rainbow table
# Testing again
pwd = Rainbow_Table[0][0] # first password in the hash chain
for i in range(0, t):
  hash = SHA256.new(pwd.encode('utf-8')) # hash it
  digest = int.from_bytes(hash.digest(), byteorder='big') # convert the hash into an integer
  pwd = Reduction(digest%pwd_space, Alphabet, pwd_len) # Reduce it
if pwd == Rainbow_Table[0][1]:
  print("The test passed:)")
else:
  print("The test failed:(")
  

# Digests
digest = [0]*10
digest[0] = 100245009005103267899033614526941913880246373596564823340949840790844809103119
digest[1] = 19975499931938919928595451537096181331883854568747045850221901234691104582098
digest[2] = 113755495174055610876492464753048312831115306302701553827210127388606508241384
digest[3] = 91716148188179664717616297774779369080831030621153106066937072640936294082436
digest[4] = 114327333148588727761456040560697699459972533926123848855642209266882904981056
digest[5] = 114092167432998812840496186716627935081797792706490494942204367130254495731666
digest[6] = 38281036052010144447899334632289647459864065649722502224373489543446886678643
digest[7] = 44545357949490023150618582332141371853866888964826995324110314901909474805088
digest[8] = 38048259072653533075550911757874348323176766191918852427444568385091382449858
digest[9] = 35430391149852444211048461076529046528250550719267058178400921942117732723330

print("\The mission is to find six-character passwords that correspond to these digests:\n")
print(digest)

for k in range(0,10):
  x = Reduction(digest[k] % pwd_space, Alphabet, pwd_len)  
  for i in range(0, len(Rainbow_Table)):      
   if(i != len(Rainbow_Table) - 1):
      if x == Rainbow_Table[i][1]:

         print("digest[" + str(k) +  "]= " + Rainbow_Table[i][0])
         break
   else:        # to be sure that there is no out of range error
     if x == Rainbow_Table[len(Rainbow_Table) - 1][1]:

       print("The password for digest[" + str(k) + "]= " + Rainbow_Table[len(Rainbow_Table) - 1][0])
       break
     else:            # case 2 starts here if case1 fails to find the password
       print("digest[" + str(k)  + "] case2...")
       bool = 0
       digest_d = digest[k]
       while bool== 0:
         x2 = Reduction(digest_d % pwd_space, Alphabet, pwd_len)
         hash = SHA256.new(x2.encode('utf-8'))  # hash it
         digest_d = int.from_bytes(hash.digest(), byteorder='big')  # convert the hash into an integer
         x2 = Reduction(digest_d % pwd_space, Alphabet, pwd_len)  # Reduce it
         for i in range(0, len(Rainbow_Table)):
           if x2 == Rainbow_Table[i][1]:

             print("digest[" + str(k) + "] " + Rainbow_Table[i][0])
             bool = 1
             break