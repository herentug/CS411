ciphertext="A RRNNQW TB IGQOEE BAYL QHMLRAOA WG RZE TZHSFDF BAYL I QWG'R CNBE MFW AAAPCJ."
ciphertext=ciphertext.lower()
lowercase = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8,
         'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14, 'p':15, 'q':16,
         'r':17, 's':18,  't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24,
         'z':25}

inv_lowercase = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i',
         9:'j', 10:'k', 11:'l', 12:'m', 13:'n', 14:'o', 15:'p', 16:'q',
         17:'r', 18:'s', 19:'t', 20:'u', 21:'v', 22:'w', 23:'x', 24:'y',
         25:'z'}

key="qpaesib"
key=key.lower()
key=key*((len(ciphertext)/len(key))+1)  # lazy way to rotate the key :)


plaintext=""
i=0
j=0

while(ciphertext[i]!='.'):
    if (ciphertext[i].isalpha()):
        a=lowercase[ciphertext[i]]
        b=lowercase[key[j]]
        c = (a - b)%26
        d =inv_lowercase[c]
        plaintext += (inv_lowercase[(lowercase[ciphertext[i]] - lowercase[key[j]])%26])
        j+=1
        
    else:
        plaintext += ciphertext[i]
    i+=1

plaintext=plaintext.upper()
print(plaintext)