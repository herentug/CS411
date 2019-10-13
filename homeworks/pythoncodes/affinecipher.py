import hw01_helper as h

def gcd(x, y): 
  
   while(y): 
       x, y = y, x % y 
  
   return x 


text="? RCYYP FYYK?VISYY?.J,HGQL?. ,HU!O,HXVBKMBRY??EPYT"

text=text.upper()
for b in range(1,30,2):
    for a in range(1,30):
            if(gcd(a,b)==1):
                k = h.key()
                k.gamma=a
                k.theta=b
                plain= h.Affine_Dec(text,k)
                
                print(str(a) + "-" + str(b) + "\t:" + plain)
