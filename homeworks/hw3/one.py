import itertools
from functools import reduce

ms1 = ms2 = polyred = None


def setGF2(degree, irPoly):
    def i2P(sInt): # We are converting an integer into a polynomial
        
        return [(sInt >> i) & 1
                for i in reversed(range(sInt.bit_length()))]

    global ms1, ms2, polyred
    ms1 = ms2 = 1 << degree
    ms2 -= 1
    polyred = reduce(lambda x, y: (x << 1) + y, i2P(irPoly)[1:])


def multiplication_in_GF(p1, p2): 
    p = 0
    while p2:
        if p2 & 1:
            p ^= p1
        p1 <<= 1
        if p1 & ms1:
            p1 ^= polyred
        p2 >>= 1
    return p & ms2



setGF2(8, 0b100011011)  # x^8 + x^4 + x^3 + x + 1
   

multiplcation_result = multiplication_in_GF(0b11011101, 0b11111000)
val = format(multiplcation_result, "b")
val = list(val)

print(val)