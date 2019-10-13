import numpy as np

cipher="gsoomonyosppwrolraqlgsykesfngsiopgtcpioqfsrpvetdzqptdwmfrsesqdkxztomwlodtkxhhxrhazwsyhapkzgsdwkwvrptlhchvsehovgvwjleblkosonawledtppamuttmcwdbeoobgogttdwmskqanuznedejmsqlptsmwmdseswgcclnznjnjpnhicddsezijjodtadwmsygknlgojewzzdqtvaazhcsanvwrcmehtkzcsagmlnkdkenlgoceeaknwpmealzuptdmgmvjoppwqczujl'ksrpssmwoyqewaqvsydwvvcyhnundzuptdmonyoswzwkygehgvzbvajlvdoabqbagkgelzglsdeobgjoppwvvlsweobgfymebwjdsdlamhzxometwrdzgkjweyceeaddoa"

alphabet = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8,
         'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14, 'p':15, 'q':16,
         'r':17, 's':18,  't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24,
         'z':25}

substr=[""]*7
k=[0]*7



freq=[0.0]*26


for i in range(0,7):
    j=i
    while(j <= len(cipher)-1):
        substr[i]+=cipher[j]
        j+=7
    
print(substr)

text="gogrroypwebklcdsqckwvsvzkdlldrd"

total=len(text)

text=text.lower()
for i in text:
    if(i.isalpha()):
        alphabet[i]+= 1

for i in alphabet:
    freq[alphabet[i]]= float(alphabet[i])/total

#print(freq)

letfreq=[8.55,1.60,3.16,3.87,12.10,2.18,2.09,4.96,7.33,0.22,0.81,4.21,2.53,7.17,7.47,2.07,0.10,6.33,6.73,8.94,2.68,1.06,1.83,0.19,1.72,0.11]
texfreq=[0.0]*26
possible_fitnesses=[0.0]*26

for i in range (0,26):
    fitness=pow(np.array(letfreq),2)-pow(np.array(freq),2)
    fitness=abs(fitness)
    possible_fitnesses[i]=sum(fitness)

    temp=letfreq.pop(0)
    letfreq.append(temp)
    #print(letfreq)




possible_fitnesses.sort()
print(possible_fitnesses)


