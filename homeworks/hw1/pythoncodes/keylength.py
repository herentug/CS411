coincides = [0]*26


plain=""
cipher="Gsoom onyos ppwro lra Q lgsyk E sfng.\nSio pgtcp io qf srp vetdzqp, tdwmfr;\nSe sqdk xzt omw lo dtkxhhxr hazw\nSy hapkz gsd wkwvr ptlh ch vseh ovgv.\nWj leblko sonaw ledt ppamu tt mcwdb\nEo obgo gttdwms k qanuznede jmsq\nLptsmwm dse swgcc lnz njnjpn hicd\nDse zijjodt adwmsyg kn lgo jewz.\n\nZd qtvaa zhc sanvwrc mehtk z csagm\nLn kdk en lgoce ea knwp mealzup.\nTdm gmvj oppwq czujl'k srp ssmwo\nYq ewaq vsyd wvv cyhnu ndzup.\nTdm onyos wzw kygehg, vzbv ajl vdoa,\nBqb A gkge lzglsdeo bg jopp,\nWvv lsweo bg fy mebwjd S dlamh,\nZxo metwr dz gk jweyce E addoa."

def delspace(s):
    s=s.lower()
    s2=""
    for i in range(0,len(s)):
        if(s[i]!=' ' and s[i]!='\n' and s[i]!=',' and s[i]!='.' and s[i]!=';'):
            s2+= s[i]

    return s2

cipher_modified=delspace(cipher)
compare=cipher_modified*2

print(cipher_modified)
for i in range(1,26):
    for j in range(0,len(cipher_modified)):
        if(cipher_modified[j]==compare[j+i]):
            coincides[i]+=1


l=coincides.index(max(coincides))
print(coincides)
print(l)
