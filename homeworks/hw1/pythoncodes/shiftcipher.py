alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
plaintext="NZWO"
ciphertext=""
solutions=[]
plaintext=plaintext.lower()


for offset in range(0,26):

    for i in range(0,len(plaintext)):
        ciphertext+=alphabet[(alphabet.index(plaintext[i])+offset)%26]
        
    solutions.append(ciphertext)
    ciphertext=""

print(solutions)